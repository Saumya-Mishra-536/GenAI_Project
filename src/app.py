import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
from pathlib import Path
import sys
import os
import json
from utils import apply_terminal_theme, print_terminal_log

# Setup path for agent imports - handle both local and deployed scenarios
_root = Path(__file__).parent.parent
_backend_path = _root / 'End_sem' / 'backend'
if _backend_path.exists() and str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

st.set_page_config(
    page_title="NEURAL GRID | EV FORECAST",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_terminal_theme()

# ==========================================
# Cached Model & Agent Loaders
# ==========================================

@st.cache_resource
def load_model():
    try:
        # Try multiple possible paths for the model file
        possible_paths = [
            'models/ev_demand_timeseries.pkl',
            'src/models/ev_demand_timeseries.pkl',
            Path(__file__).parent / 'models' / 'ev_demand_timeseries.pkl',
        ]
        
        for path in possible_paths:
            model_path = Path(path)
            if model_path.exists():
                return joblib.load(model_path)
        
        st.warning("Warning: Model file not found.")
        return None
    except Exception as e:
        st.error(f"Model Loading Error: {str(e)}")
        return None

@st.cache_resource
def load_agent():
    try:
        from agent.run_agent import run_planning_agent
        return run_planning_agent
    except Exception as e:
        st.warning(f"Warning: Agent system not available: {str(e)}")
        return None

predictor = load_model()
agent_runner = load_agent()

# ==========================================
# Data Processing Functions
# ==========================================

def preprocess_data(df_raw):
    """
    Transforms raw station CSV format into model-ready features.
    """
    df = df_raw.copy()
    try:
        # 1. Temporal Features
        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='mixed')
        df['Hour'] = df['Datetime'].dt.hour
        df['DayOfWeek'] = df['Datetime'].dt.dayofweek
        
        # 2. Time-Series Memory (Lags & Rolling)
        target_col = 'EV Charging Demand (kW)'
        df['Demand_Lag_1'] = df[target_col].shift(1)
        df['Demand_Lag_2'] = df[target_col].shift(2)
        df['Rolling_Avg_3h'] = df[target_col].rolling(window=3).mean().shift(1)
        
        # Use bfill() and ffill() instead of deprecated method parameter
        df = df.bfill().ffill()
        return df
    except Exception as e:
        st.error(f"Processing Error: {str(e)}")
        return None

def run_agent_workflow(processed_df):
    """Run the agentic planning pipeline on processed data."""
    if agent_runner is None:
        st.error("Agent system unavailable. Install langchain and langgraph packages.")
        return None
    
    try:
        with st.spinner("Running agent planning pipeline..."):
            result = agent_runner(processed_df)
            return result
    except Exception as e:
        st.error(f"Agent Error: {str(e)}")
        return None

# ==========================================
# UI Components
# ==========================================

st.title("NEURAL GRID: EV DEMAND FORECASTING")
st.markdown("*Intelligent forecasting and infrastructure planning for EV charging networks*")
st.markdown("---")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Manual Prediction",
    "Batch Analysis",
    "Agent Planning",
    "Dashboard"
])

# ==========================================
# TAB 1: Manual Prediction
# ==========================================

with tab1:
    col_input, col_viz = st.columns([1, 2])
    
    with col_input:
        st.subheader("Input Parameters")
        h = st.slider("Hour (0-23)", 0, 23, 12)
        d = st.slider("Day (0=Mon, 6=Sun)", 0, 6, 0)
        l1 = st.number_input("Demand Lag-1 (kW)", value=0.1500, format="%.4f")
        l2 = st.number_input("Demand Lag-2 (kW)", value=0.1450, format="%.4f")
        r3 = st.number_input("Rolling 3h (kW)", value=0.1480, format="%.4f")
        pr = st.number_input("Price ($/kWh)", value=0.1200, format="%.4f")
        stb = st.number_input("Stability Index", value=1.0000, format="%.4f")
        evc = st.number_input("EV Count", value=5)

        if st.button("RUN INFERENCE", key="inference_btn"):
            if predictor:
                features = [h, d, l1, l2, r3, pr, stb, evc]
                prediction = predictor.predict([features])[0]
                st.metric("PREDICTED LOAD", f"{prediction:.4f} kW", delta=f"{prediction*1000:.0f} W")
            else:
                st.error("Error: Model file not found.")

    with col_viz:
        st.subheader("Load Profile")
        x = np.linspace(0, 23, 100)
        y = 0.15 + 0.1 * np.sin((x - 6) * np.pi / 12)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x, y=y, fill='tozeroy',
            line=dict(color='#00f2ff', width=2),
            fillcolor='rgba(0, 242, 255, 0.2)',
            name='Load Profile'
        ))
        fig.add_trace(go.Scatter(
            x=[h], y=[0.15 + 0.1 * np.sin((h - 6) * np.pi / 12)],
            mode='markers',
            marker=dict(color='#ff1493', size=12),
            name='Current Hour'
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 2: Batch Analysis
# ==========================================

with tab2:
    st.subheader("📁 Upload & Process Station Data")
    st.write("Upload CSV or Excel file with charging station data")
    
    uploaded_file = st.file_uploader(
        "Select CSV or Excel",
        type=["csv", "xlsx"],
        key="batch_upload"
    )
    
    if uploaded_file and predictor:
        try:
            raw_data = (
                pd.read_csv(uploaded_file)
                if uploaded_file.name.endswith('.csv')
                else pd.read_excel(uploaded_file)
            )
            
            print_terminal_log(f"Loaded {len(raw_data)} records from {uploaded_file.name}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Records", len(raw_data))
            with col2:
                st.metric("Columns", len(raw_data.columns))
            with col3:
                st.metric("Date Range", f"{raw_data['Date'].min()} to {raw_data['Date'].max()}")
            
            if st.button("⚙️ PROCESS & PREDICT", key="batch_process"):
                processed_df = preprocess_data(raw_data)
                
                if processed_df is not None:
                    model_features = [
                        'Hour', 'DayOfWeek', 'Demand_Lag_1', 'Demand_Lag_2',
                        'Rolling_Avg_3h', 'Electricity Price ($/kWh)',
                        'Grid Stability Index', 'Number of EVs Charging'
                    ]
                    
                    X = processed_df[model_features]
                    processed_df['AI_Predicted_Demand_kW'] = predictor.predict(X)
                    
                    print_terminal_log("✅ Inference complete")
                    
                    # Show results
                    st.subheader("Results Preview")
                    st.dataframe(
                        processed_df[[
                            'Date', 'Time', 'EV Charging Demand (kW)',
                            'AI_Predicted_Demand_kW'
                        ]].head(10),
                        use_container_width=True
                    )
                    
                    # Metrics
                    actual = processed_df['EV Charging Demand (kW)'].values
                    predicted = processed_df['AI_Predicted_Demand_kW'].values
                    mae = np.mean(np.abs(actual - predicted))
                    rmse = np.sqrt(np.mean((actual - predicted) ** 2))
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Mean Absolute Error", f"{mae:.4f} kW")
                    with col2:
                        st.metric("RMSE", f"{rmse:.4f} kW")
                    with col3:
                        st.metric("Records Processed", len(processed_df))
                    
                    # Download results
                    csv_buffer = BytesIO()
                    processed_df.to_csv(csv_buffer, index=False)
                    csv_buffer.seek(0)
                    
                    st.download_button(
                        "📥 DOWNLOAD RESULTS",
                        csv_buffer.getvalue(),
                        "predictions.csv",
                        "text/csv"
                    )
                    
                    # Visualization
                    st.subheader("Prediction vs Actual")
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=processed_df.index,
                        y=processed_df['EV Charging Demand (kW)'],
                        name='Actual',
                        line=dict(color='#00f2ff')
                    ))
                    fig.add_trace(go.Scatter(
                        x=processed_df.index,
                        y=processed_df['AI_Predicted_Demand_kW'],
                        name='Predicted',
                        line=dict(color='#ff1493', dash='dash')
                    ))
                    fig.update_layout(
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        hovermode='x unified',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

# ==========================================
# TAB 3: Agent Planning
# ==========================================

with tab3:
    st.subheader("🤖 Infrastructure Planning Agent")
    st.write("Upload data to run the AI planning agent for intelligent infrastructure recommendations")
    
    uploaded_file_agent = st.file_uploader(
        "Select CSV or Excel",
        type=["csv", "xlsx"],
        key="agent_upload"
    )
    
    if uploaded_file_agent:
        try:
            raw_data = (
                pd.read_csv(uploaded_file_agent)
                if uploaded_file_agent.name.endswith('.csv')
                else pd.read_excel(uploaded_file_agent)
            )
            
            processed_df = preprocess_data(raw_data)
            
            if st.button("🚀 RUN AGENT PLANNING", key="run_agent"):
                result = run_agent_workflow(processed_df)
                
                if result:
                    st.session_state.agent_result = result
                    st.success("✅ Agent planning completed!")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Display agent results if available
    if "agent_result" in st.session_state:
        result = st.session_state.agent_result
        
        # Insights Section
        if result.get("insights"):
            insights = result["insights"]
            st.subheader("📊 Demand Insights")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Risk Level", insights.get("risk_level", "Unknown"))
            with col2:
                st.metric("Max Demand", f"{insights.get('max_demand', 0):.2f} kW")
            with col3:
                st.metric("Avg Demand", f"{insights.get('avg_demand', 0):.2f} kW")
            with col4:
                st.metric("Peak Hours", str(insights.get("peak_hours", [])))
        
        # Patterns Section
        if result.get("patterns"):
            patterns = result["patterns"]
            st.subheader("🔍 Pattern Detection")
            st.info(f"**Key Patterns**: {patterns.get('summary', 'Patterns detected')}")
        
        # Planning Section
        if result.get("final_plan"):
            plan = result["final_plan"]
            st.subheader("📋 Infrastructure Plan")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Confidence Score", f"{plan.get('confidence_score', 0):.2%}")
            with col2:
                st.metric("Risk Level", plan.get("risk_level", "Unknown"))
            
            # Recommendations
            if plan.get("recommendations"):
                st.subheader("🎯 Recommendations")
                for i, rec in enumerate(plan["recommendations"], 1):
                    with st.expander(f"**#{i}** {rec.get('action', 'Action')} - {rec.get('priority', 'medium').upper()}"):
                        st.write(f"**Type**: {rec.get('type', 'N/A')}")
                        st.write(f"**Location**: {rec.get('location', 'N/A')}")
                        st.write(f"**Justification**: {rec.get('justification', 'N/A')}")
                        if rec.get('estimated_cost'):
                            st.write(f"**Est. Cost**: ${rec.get('estimated_cost'):,.0f}")
        
        # Simulation Results
        if result.get("simulated_impact"):
            impact = result["simulated_impact"]
            st.subheader("🎲 Simulated Scenarios")
            st.info(f"**Scenario**: {impact.get('scenario', 'Peak stress test')}")
            st.write(f"**Impact**: {impact.get('impact_analysis', 'Analysis results')}")
            st.metric("Robustness Score", f"{impact.get('robustness_score', 0):.2%}")
        
        # Full State JSON (Advanced)
        if st.checkbox("Show Full Agent State (Advanced)"):
            st.json(result)

# ==========================================
# TAB 4: Dashboard
# ==========================================

with tab4:
    st.subheader("Analytics Dashboard")
    st.write("Real-time monitoring and analytics for EV charging infrastructure")
    
    # Synthetic data for demo
    hours = list(range(24))
    demand = [10 + 8 * (1 + 0.5 * ((h - 12) ** 2 / 144)) + (2 if h % 2 == 0 else -1) for h in hours]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Hourly Demand")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=hours, y=demand,
            marker=dict(color='#00f2ff'),
            name='Demand'
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("System Status")
        metrics_data = {
            "Active Chargers": 150,
            "Utilization": 72,
            "Grid Health": 95,
            "Network Load": 58
        }
        
        for metric, value in metrics_data.items():
            st.metric(metric, f"{value}%")
    
    # Day of week analysis
    st.subheader("Weekly Pattern")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_demand = [85.2, 87.5, 88.1, 86.9, 89.2, 72.3, 68.9]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days, y=day_demand,
        mode='lines+markers',
        line=dict(color='#00f2ff', width=3),
        marker=dict(size=10),
        name='Avg Demand'
    ))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
print_terminal_log("System Idle. Awaiting data packet...")