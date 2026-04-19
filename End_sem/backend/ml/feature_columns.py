"""
Single source of truth for model feature names and manual API mapping.
"""

import math
from typing import Dict, List, Any

# Order matters for model input rows
BASE_FEATURES: List[str] = [
    "Hour",
    "DayOfWeek",
    "hour_sin",
    "hour_cos",
    "dow_sin",
    "dow_cos",
    "Demand_Lag_1",
    "Demand_Lag_2",
    "Demand_Lag_3",
    "Rolling_Avg_3h",
    "Rolling_Avg_6h",
    "Rolling_Std_3h",
    "Electricity Price ($/kWh)",
    "Grid Stability Index",
    "Number of EVs Charging",
    "Price_Hour_Interact",
    "Price_EV_Interact",
]

# Optional exogenous signals present in station CSVs (filled with medians or 0)
EXTRA_NUMERIC_FEATURES: List[str] = [
    "Solar Energy Production (kW)",
    "Wind Energy Production (kW)",
    "Charging Station Capacity (kW)",
    "Peak Demand (kW)",
    "Renewable Energy Usage (%)",
    "EV Charging Efficiency (%)",
    "Battery Storage (kWh)",
    "Total Renewable Energy Production (kW)",
]


def full_feature_list(include_extras: bool = True) -> List[str]:
    return BASE_FEATURES + (EXTRA_NUMERIC_FEATURES if include_extras else [])


def add_cyclical_time_features(df):
    """Mutates df with sin/cos encodings (expects Hour, DayOfWeek)."""
    import numpy as np

    h = df["Hour"].astype(float)
    d = df["DayOfWeek"].astype(float)
    df["hour_sin"] = np.sin(2 * np.pi * h / 24.0)
    df["hour_cos"] = np.cos(2 * np.pi * h / 24.0)
    df["dow_sin"] = np.sin(2 * np.pi * d / 7.0)
    df["dow_cos"] = np.cos(2 * np.pi * d / 7.0)
    return df


def build_manual_feature_vector(features: Dict[str, Any], defaults: Dict[str, float], columns: List[str]) -> List[float]:
    """
    Map API payload (hour, day, lag1, ...) to training column order.
    `defaults` supplies medians for columns not in the manual form (e.g. solar).
    """
    h = float(features.get("hour", 12))
    d = float(features.get("day", 0))
    pr = float(features.get("price", 0.12))
    evc = float(features.get("ev_count", 5))
    stab = float(features.get("stability", 1.0))

    manual_map = {
        "Hour": h,
        "DayOfWeek": d,
        "hour_sin": math.sin(2 * math.pi * h / 24.0),
        "hour_cos": math.cos(2 * math.pi * h / 24.0),
        "dow_sin": math.sin(2 * math.pi * d / 7.0),
        "dow_cos": math.cos(2 * math.pi * d / 7.0),
        "Demand_Lag_1": float(features.get("lag1", 0.15)),
        "Demand_Lag_2": float(features.get("lag2", 0.145)),
        "Demand_Lag_3": float(features.get("lag3", 0.14)),
        "Rolling_Avg_3h": float(features.get("rolling3", 0.148)),
        "Rolling_Avg_6h": float(features.get("rolling6", 0.146)),
        "Rolling_Std_3h": float(features.get("std3", 0.01)),
        "Electricity Price ($/kWh)": pr,
        "Grid Stability Index": stab,
        "Number of EVs Charging": float(evc),
        "Price_Hour_Interact": pr * h,
        "Price_EV_Interact": pr * evc,
    }

    row = []
    for col in columns:
        if col in manual_map:
            row.append(manual_map[col])
        else:
            row.append(float(defaults.get(col, 0.0)))
    return row
