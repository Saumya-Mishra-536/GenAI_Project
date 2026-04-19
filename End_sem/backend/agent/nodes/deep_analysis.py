import pandas as pd
from typing import Dict, Any

def deep_analyze_demand(state: Dict[str, Any]) -> Dict[str, Any]:
    """Triggered conditionally if Risk is High. Calculates variance and deeper pattern stats."""
    df = state.get('df_raw')
    insights = state.get('insights', {})

    if df is not None and not (hasattr(df, 'empty') and df.empty):
        target_col = 'AI_Predicted_Demand_kW' if 'AI_Predicted_Demand_kW' in df.columns else 'EV Charging Demand (kW)'
        variance = float(df[target_col].var())
        insights["demand_variance"] = round(variance, 6)
        insights["deep_analysis_note"] = (
            "High volatility detected via deep analysis node. "
            "Grid stabilization is urgently required."
        )

        # Additional deep stats for frontend
        if 'Datetime' in df.columns:
            daily_max = df.groupby(df['Datetime'].dt.date)[target_col].max()
            insights["peak_day"] = str(daily_max.idxmax()) if len(daily_max) > 0 else "Unknown"
            insights["daily_peak_avg"] = round(float(daily_max.mean()), 4)

    return {"insights": insights}
