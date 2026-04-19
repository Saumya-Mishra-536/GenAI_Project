import pandas as pd
from typing import Dict, Any

def detect_patterns(state: Dict[str, Any]) -> Dict[str, Any]:
    """Detects correlations and repeated congestion patterns in the data."""
    df = state.get('df_raw')

    patterns = {
        "repeated_congestion": "Unidentified",
        "price_correlation": "Pending calculation",
        "grid_stability_impact": "Pending calculation"
    }

    if df is None or (hasattr(df, 'empty') and df.empty):
        return {"patterns": patterns}

    try:
        target_col = 'AI_Predicted_Demand_kW' if 'AI_Predicted_Demand_kW' in df.columns else 'EV Charging Demand (kW)'

        if 'Electricity Price ($/kWh)' in df.columns:
            corr_price = df[target_col].corr(df['Electricity Price ($/kWh)'])
            patterns["price_correlation"] = f"Correlation: {corr_price:.4f}"
            patterns["price_correlation_value"] = round(float(corr_price), 4)

        if 'Grid Stability Index' in df.columns:
            corr_grid = df[target_col].corr(df['Grid Stability Index'])
            patterns["grid_stability_impact"] = f"Correlation: {corr_grid:.4f}"
            patterns["grid_stability_value"] = round(float(corr_grid), 4)

        if 'Number of EVs Charging' in df.columns:
            corr_ev = df[target_col].corr(df['Number of EVs Charging'])
            patterns["ev_count_correlation"] = f"Correlation: {corr_ev:.4f}"
            patterns["ev_count_correlation_value"] = round(float(corr_ev), 4)

        insights = state.get('insights', {})
        if insights.get("risk_level") == "High":
            patterns["repeated_congestion"] = "Found repeated peaks at prime hours causing sustained high load."
        else:
            patterns["repeated_congestion"] = "Sporadic congestion, no sustained risk."

    except Exception as e:
        patterns["error"] = str(e)

    return {"patterns": patterns}
