"""
NEURAL GRID v2 — Streamlit Dashboard
Alternative UI for the EV Charging Demand Platform.
Run: streamlit run backend/streamlit_app.py
"""
import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO
from sklearn.metrics import r2_score, mean_absolute_error
import sys
import os
import json

# Setup paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import OPENROUTER_API_KEY

try:
    from agent.run_agent import run_planning_agent
except Exception as e:
    run_planning_agent = None
    print(f"Warning: agent module failed to load. {e}")


# ──────────────────────────────────────
# Theme & Styling
# ──────────────────────────────────────

st.set_page_config(page_title="NEURAL GRID v2 | EV FORECAST", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #050510 0%, #0a0a1a 50%, #050510 100%);
    color: #e0e0e0;
    font-family: 'Inter', sans-serif;
}

/* Glowing buttons */
@keyframes pulse-glow {
    0% { border-color: #00f2ff; box-shadow: 0 0 5px rgba(0,242,255,0.3); }
    50% { border-color: #00f2ff; box-shadow: 0 0 20px rgba(0,242,255,0.5); }
    100% { border-color: #00f2ff; box-shadow: 0 0 5px rgba(0,242,255,0.3); }
}

.stButton>button {
    width: 100%;
    background: linear-gradient(135deg, rgba(0,242,255,0.1), rgba(0,242,255,0.05)) !important;
    color: #00f2ff !important;
    border: 1px solid #00f2ff !important;
    border-radius: 8px !important;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    animation: pulse-glow 3s infinite;
    transition: all 0.3s ease;
    font-family: 'Inter', sans-serif;
}

.stButton>button:hover {
    background: linear-gradient(135deg, rgba(0,242,255,0.2), rgba(0,242,255,0.1)) !important;
    box-shadow: 0 0 30px rgba(0,242,255,0.6) !important;
}

/* Terminal text */
.terminal-text {
    color: #00ff41;
    font-family: 'Courier New', monospace;
    font-size: 0.78rem;
    margin: 0;
    padding: 2px 0;
    opacity: 0.8;
}

/* Metrics */
div[data-testid="stMetricValue"] {
    color: #00f2ff !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
}

.stDataFrame {
    border: 1px solid rgba(0,242,255,0.2);
    border-radius: 8px;
}

div[data-testid="stFileUploader"] {
    border: 1px dashed rgba(0,242,255,0.4);
    background: rgba(0,242,255,0.03);
    padding: 15px;
    border-radius: 8px;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    color: #888 !important;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    color: #00f2ff !important;
}
</style>
""", unsafe_allow_html=True)


def print_terminal_log(message):
    st.markdown(f'<p class="terminal-text">[SYSTEM]: {message}</p>', unsafe_allow_html=True)


# ──────────────────────────────────────
# Model Loading
# ──────────────────────────────────────

@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        model = joblib.load(os.path.join(base_dir, 'models', 'ev_demand_timeseries.pkl'))
        try:
            scaler = joblib.load(os.path.join(base_dir, 'models', 'scaler.pkl'))
        except Exception:
            scaler = None
        return model, scaler
    except Exception as e:
        st.error(f"Prediction model not found: {e}")
        return None, None


predictor, scaler = load_model()

from ml.preprocessor import preprocess_data


# ──────────────────────────────────────
# Dashboard
# ──────────────────────────────────────

st.title("⚡ NEURAL GRID v2: EV DEMAND FORECASTING")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["⚙️ Manual Prediction", "📊 Batch Processing", "🤖 AI Infrastructure Planner"])

with tab1:
    col_input, col_viz = st.columns([1, 2])
    with col_input:
        h = st.slider("Hour", 0, 23, 12)
        d = st.slider("Day (0=Mon, 6=Sun)", 0, 6, 0)
        l1 = st.number_input("Demand Lag-1 (kW)", value=0.1500, format="%.4f")
        l2 = st.number_input("Demand Lag-2 (kW)", value=0.1450, format="%.4f")
        l3 = st.number_input("Demand Lag-3 (kW)", value=0.1400, format="%.4f")
        r3 = st.number_input("Rolling 3h (kW)", value=0.1480, format="%.4f")
        r6 = st.number_input("Rolling 6h (kW)", value=0.1460, format="%.4f")
        rst3 = st.number_input("Rolling Std 3h", value=0.0100, format="%.4f")
        pr = st.number_input("Price ($/kWh)", value=0.1200, format="%.4f")
        stb = st.number_input("Stability Index", value=1.0000, format="%.4f")
        evc = st.number_input("EV Count", value=5)

        if st.button("RUN INFERENCE"):
            if predictor and scaler:
                price_hour = pr * h
                price_ev = pr * evc
                features = np.array([[h, d, l1, l2, l3, r3, r6, rst3, pr, stb, evc, price_hour, price_ev]], dtype=float)
                features_scaled = scaler.transform(features)
                prediction = predictor.predict(features_scaled)[0]
                st.metric("PREDICTED LOAD", f"{prediction:.4f} kW")
            else:
                st.error("Model Error: Serialization or Scaler file not detected.")

    with col_viz:
        x = np.linspace(0, 23, 100)
        y = 0.15 + 0.1 * np.sin((x - 6) * np.pi / 12)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', line=dict(color='#00f2ff', width=2), name='Load Profile'))
        fig.add_trace(go.Scatter(
            x=[h], y=[0.15 + 0.1 * np.sin((h - 6) * np.pi / 12)],
            mode='markers', marker=dict(color='#ff3366', size=14, symbol='diamond'),
            name='Selected Hour'
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title="Daily Load Profile Curve",
            xaxis_title="Hour",
            yaxis_title="Demand (kW)",
            font=dict(family="Inter")
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Process Raw Station Data")
    st.write("Upload a raw station file (e.g., Charging station_C__Calif.csv)")
    uploaded_file = st.file_uploader("Select CSV or Excel", type=["csv", "xlsx"])

    if uploaded_file and predictor and scaler:
        raw_data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        print_terminal_log("Raw stream detected. Commencing feature engineering...")

        if st.button("EXECUTE BATCH INFRASTRUCTURE ANALYSIS"):
            try:
                processed_df = preprocess_data(raw_data)

                if processed_df is not None:
                    model_features = [
                        'Hour', 'DayOfWeek', 'Demand_Lag_1', 'Demand_Lag_2', 'Demand_Lag_3',
                        'Rolling_Avg_3h', 'Rolling_Avg_6h', 'Rolling_Std_3h',
                        'Electricity Price ($/kWh)', 'Grid Stability Index', 'Number of EVs Charging',
                        'Price_Hour_Interact', 'Price_EV_Interact'
                    ]

                    X = processed_df[model_features].astype(float)
                    X_scaled = scaler.transform(X)
                    processed_df['AI_Predicted_Demand_kW'] = predictor.predict(X_scaled)

                    y_true = processed_df['EV Charging Demand (kW)']
                    y_pred = processed_df['AI_Predicted_Demand_kW']
                    r2 = r2_score(y_true, y_pred)
                    mae = mean_absolute_error(y_true, y_pred)

                    st.success(f"Inference Complete — R² Score: {r2:.4f} | MAE: {mae:.4f}")

                    st.markdown("### Model Validation: Actual vs Predicted")
                    fig_val = go.Figure()
                    fig_val.add_trace(go.Scatter(
                        y=y_true.head(100), mode='lines',
                        name='Actual', line=dict(color='#00ff88', width=2)
                    ))
                    fig_val.add_trace(go.Scatter(
                        y=y_pred.head(100), mode='lines',
                        name='Predicted', line=dict(color='#ff00ff', dash='dash', width=2)
                    ))
                    fig_val.update_layout(template="plotly_dark", height=400, font=dict(family="Inter"))
                    st.plotly_chart(fig_val, key="val_plot", use_container_width=True)

                    st.dataframe(processed_df[['Date', 'Time', 'EV Charging Demand (kW)', 'AI_Predicted_Demand_kW']].head(20))

                    csv_buffer = BytesIO()
                    processed_df.to_csv(csv_buffer, index=False)
                    st.download_button("DOWNLOAD PREDICTIONS CSV", csv_buffer.getvalue(), "Inference_Report.csv", "text/csv")

                    st.session_state['processed_df'] = processed_df
            except Exception as e:
                st.error(f"Processing Error: {str(e)}")

st.markdown("---")
print_terminal_log("System Idle. Awaiting data packet...")

with tab3:
    st.subheader("🤖 Agentic EV Infrastructure Planner")
    st.write("Reason over predicted demand & retrieve planning guidelines using LangGraph + RAG pipeline.")

    if st.button("RUN AGENTIC PLANNER"):
        if 'processed_df' in st.session_state and st.session_state['processed_df'] is not None:
            df_to_use = st.session_state['processed_df']

            with st.spinner("Agent is reasoning... (This might take a moment)"):
                try:
                    if run_planning_agent is not None:
                        result = run_planning_agent(df_to_use)

                        insights = result.get("insights", {})
                        reasoning = result.get("reasoning", {})
                        plan = result.get("final_plan", {})
                        sim = result.get("simulated_impact", {})
                        knowledge = result.get("retrieved_knowledge", [])
                        iters = result.get("iteration_count", 0)

                        st.markdown("## 📊 Executive Summary")
                        col_risk, col_conf, col_loop = st.columns(3)
                        col_risk.metric("Risk Level", plan.get("risk_level", "Unknown"))
                        col_conf.metric("Confidence", f"{plan.get('confidence_score', 0.0)*100:.1f}%")
                        col_loop.metric("Optimization Loops", iters)

                        st.markdown("---")

                        st.markdown("### 📈 Core Demand Insights")
                        col_it, col_iv = st.columns([1, 1.5])
                        with col_it:
                            st.markdown(f"**Max Demand:** {insights.get('max_demand', 0):.2f} kW")
                            st.markdown(f"**Avg Demand:** {insights.get('avg_demand', 0):.2f} kW")
                            st.markdown(f"**Peak Hours:** {', '.join(map(str, insights.get('peak_hours', [])))}")
                            if insights.get("deep_analysis_note"):
                                st.warning(insights["deep_analysis_note"])
                        with col_iv:
                            if 'AI_Predicted_Demand_kW' in df_to_use.columns:
                                fig_trend = go.Figure()
                                fig_trend.add_trace(go.Scatter(
                                    y=df_to_use['AI_Predicted_Demand_kW'].head(150),
                                    mode='lines', fill='tozeroy',
                                    line=dict(color='#ff9900', width=2)
                                ))
                                fig_trend.update_layout(
                                    title="Predicted Load Trend",
                                    template="plotly_dark", height=250,
                                    margin=dict(l=0, r=0, t=30, b=0),
                                    font=dict(family="Inter")
                                )
                                st.plotly_chart(fig_trend, use_container_width=True)

                        st.markdown("### 🧠 AI Reasoning")
                        obs_col, inf_col, dec_col = st.columns(3)
                        with obs_col:
                            with st.expander("🔍 Observations", expanded=True):
                                for o in reasoning.get("observations", []):
                                    st.markdown(f"- {o}")
                        with inf_col:
                            with st.expander("💡 Inferences", expanded=True):
                                for i in reasoning.get("inferences", []):
                                    st.markdown(f"- {i}")
                        with dec_col:
                            with st.expander("⚡ Decisions", expanded=True):
                                for d_item in reasoning.get("decisions", []):
                                    st.markdown(f"- {d_item}")

                        st.markdown("---")
                        st.markdown("### 🚀 Infrastructure Recommendations")
                        for idx, rec in enumerate(plan.get("recommendations", [])):
                            with st.container():
                                st.markdown(f"#### Recommendation {idx+1}: {rec.get('type', 'Action').replace('_', ' ').title()}")
                                st.markdown(f"**📍 Location:** {rec.get('location', 'N/A')} &nbsp; | &nbsp; **⚡ Priority:** {rec.get('priority', 'N/A').upper()}")
                                st.info(f"**Action:** {rec.get('action', 'N/A')}")
                                st.markdown(f"**Justification:** {rec.get('justification', 'N/A')}")

                        st.markdown("---")
                        col_rag, col_sim = st.columns(2)
                        with col_rag:
                            st.markdown("### 📚 RAG Knowledge")
                            with st.container(height=300):
                                for k in knowledge:
                                    st.markdown(f"> *{k}*")
                        with col_sim:
                            st.markdown("### 🧬 Stress Simulation")
                            st.success(f"**Scenario:** {sim.get('scenario', 'Stress Test')}")
                            st.markdown(f"**Impact:** {sim.get('impact_analysis', 'No impacts logged.')}")
                            st.metric("Robustness", f"{sim.get('robustness_score', 0.0)*100:.1f}%")
                    else:
                        st.error("Agent module is missing or failed to import.")
                except Exception as e:
                    st.error("⚠️ AI Control System encountered an issue. System has safely reverted to baselines.")
        else:
            st.warning("Please upload and process data in the 'Batch Processing' tab first.")
