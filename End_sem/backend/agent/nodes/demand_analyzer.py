import pandas as pd
from typing import Dict, Any

def analyze_demand(state: Dict[str, Any]) -> Dict[str, Any]:
    """Primary demand analysis node — extracts peak hours, risk level, and load statistics."""
    df = state.get('df_raw')
    insights = {
        "peak_hours": [],
        "high_load_periods": [],
        "risk_level": "unknown",
        "message": "No data processed."
    }

    if df is None or (hasattr(df, 'empty') and df.empty):
        return {"insights": insights}

    try:
        target_col = 'AI_Predicted_Demand_kW' if 'AI_Predicted_Demand_kW' in df.columns else 'EV Charging Demand (kW)'

        # Ensure Datetime column exists
        if 'Datetime' not in df.columns:
            if 'Date' in df.columns and 'Time' in df.columns:
                df['Datetime'] = pd.to_datetime(
                    df['Date'].astype(str) + ' ' + df['Time'].astype(str),
                    format='mixed'
                )
            else:
                return {"insights": insights}

        # Peak hours based on average demand
        hourly_avg = df.groupby(df['Datetime'].dt.hour)[target_col].mean()
        peak_hours = hourly_avg.nlargest(3).index.tolist()

        # High-load periods (top 10th percentile)
        threshold = df[target_col].quantile(0.9)
        high_load_df = df[df[target_col] >= threshold]
        high_load_periods = high_load_df['Datetime'].dt.strftime('%Y-%m-%d %H:%M').tolist()[:5]

        risk_level = "High" if len(high_load_df) > len(df) * 0.15 else "Moderate"

        # Hourly distribution for frontend charts
        hourly_distribution = hourly_avg.to_dict()
        hourly_distribution = {int(k): round(float(v), 4) for k, v in hourly_distribution.items()}

        insights = {
            "peak_hours": peak_hours,
            "high_load_periods": high_load_periods,
            "risk_level": risk_level,
            "max_demand": round(float(df[target_col].max()), 4),
            "avg_demand": round(float(df[target_col].mean()), 4),
            "min_demand": round(float(df[target_col].min()), 4),
            "std_demand": round(float(df[target_col].std()), 4),
            "total_records": len(df),
            "hourly_distribution": hourly_distribution,
            "status": "Success"
        }
    except Exception as e:
        insights["message"] = f"Error during analysis: {str(e)}"

    return {"insights": insights}
