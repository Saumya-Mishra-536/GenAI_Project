import streamlit as st
import joblib
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from io import BytesIO
from utils import apply_terminal_theme, print_terminal_log

# Page Configuration
st.set_page_config(page_title="NEURAL GRID | EV FORECAST", layout="wide")
apply_terminal_theme()

# Model Loading Logic
@st.cache_resource
def load_model():
    try:
        return joblib.load('ev_demand_timeseries.pkl')
    except Exception:
        return None

predictor = load_model()

st.title("⚡ NEURAL GRID: EV DEMAND FORECASTER")
st.markdown("---")

# Navigation Tabs
tab1, tab2 = st.tabs(["Single Inference", "Batch Excel Processing"])

with tab1:
    col_input, col_viz = st.columns([1, 2])
    
    with col_input:
        st.subheader("Data Input Stream")
        target_hour = st.slider("Target Hour (24h)", 0, 23, 12)
        day_of_week = st.selectbox("Day of Week", range(7), format_func=lambda x: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][x])
        
        st.markdown("### Neural Lags")
        lag_1 = st.number_input("Demand Lag-1 (kW)", value=0.1500, format="%.4f")
        lag_2 = st.number_input("Demand Lag-2 (kW)", value=0.1450, format="%.4f")
        rolling_avg = st.number_input("Rolling 3h Average (kW)", value=0.1480, format="%.4f")
        
        st.markdown("### Environmental Factors")
        grid_price = st.slider("Electricity Price ($/kWh)", 0.05, 0.25, 0.12)
        stability = st.slider("Stability Index", 0.5, 1.5, 1.0)
        ev_count = st.number_input("Active EV Count", value=5)

        if st.button("RUN NEURAL INFERENCE"):
            if predictor:
                with st.status("Analyzing parameters...", expanded=True) as status:
                    print_terminal_log("Vectorizing input vector...")
                    # Order must match training: Hour, Day, Lag1, Lag2, Rolling3, Price, Stability, EVCount
                    feature_vector = np.array([[target_hour, day_of_week, lag_1, lag_2, rolling_avg, grid_price, stability, ev_count]])
                    prediction = predictor.predict(feature_vector)[0]
                    
                    time.sleep(0.5)
                    status.update(label="Inference Sequence Complete", state="complete")
                    
                    st.markdown("### SYSTEM OUTPUT")
                    st.metric(label="Predicted Charging Load", value=f"{prediction:.4f} kW")
                    st.balloons()
            else:
                st.error("System Error: Neural Engine (pkl) not found.")

    with col_viz:
        st.subheader("Grid Load Projection")
        x_hours = np.linspace(0, 23, 100)
        y_demand = 0.12 + 0.08 * np.sin((x_hours - 6) * np.pi / 12)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_hours, y=y_demand, fill='tozeroy', line=dict(color='#00f2ff', width=2), name='Base Load'))
        fig.add_trace(go.Scatter(x=[target_hour], y=[0.12 + 0.08 * np.sin((target_hour - 6) * np.pi / 12)], 
                                 mode='markers', marker=dict(color='red', size=15), name='Target Node'))
        
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        print_terminal_log("Visualizer updated.")

with tab2:
    st.subheader("Batch Stream Processing")
    st.write("Upload an Excel file with columns: `Hour`, `DayOfWeek`, `Demand_Lag_1`, `Demand_Lag_2`, `Rolling_Avg_3h`, `Price`, `Stability`, `EV_Count`.")
    
    uploaded_file = st.file_uploader("Upload Neural Input Stream (XLSX)", type="xlsx")
    
    if uploaded_file and predictor:
        df_input = pd.read_excel(uploaded_file)
        print_terminal_log(f"Batch Stream Detected: {len(df_input)} rows found.")
        
        if st.button("PROCESS BATCH DATA"):
            with st.status("Processing Neural Sequences...", expanded=True) as status:
                # Required feature columns
                features_list = ['Hour', 'DayOfWeek', 'Demand_Lag_1', 'Demand_Lag_2', 'Rolling_Avg_3h', 'Price', 'Stability', 'EV_Count']
                
                if all(col in df_input.columns for col in features_list):
                    X_batch = df_input[features_list]
                    df_input['AI_Predicted_Demand_kW'] = predictor.predict(X_batch)
                    
                    status.update(label="Batch Processing Complete", state="complete")
                    st.dataframe(df_input.head(10), use_container_width=True)
                    
                    # Buffer for Excel Download
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        df_input.to_excel(writer, index=False)
                    
                    st.download_button(
                        label="📥 DOWNLOAD PROCESSED RESULTS",
                        data=output.getvalue(),
                        file_name="EV_Demand_Results.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.error("Schema Mismatch: Excel columns must match the required feature set.")

st.markdown("---")
print_terminal_log("System Idle. Awaiting parameter set...")