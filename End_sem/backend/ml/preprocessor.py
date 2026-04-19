import pandas as pd
import numpy as np
from typing import Optional

from .dataset import engineer_features_for_station, resolve_target_column
from .feature_columns import full_feature_list

# Populated after first predictor load; safe default for imports before model exists
MODEL_FEATURES = full_feature_list(True)


def preprocess_data(df_raw: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Transforms raw station CSV into model-ready features (aligned with training pipeline).
    """
    df = df_raw.copy()

    if "Datetime" not in df.columns:
        if "Date" in df.columns and "Time" in df.columns:
            df["Datetime"] = pd.to_datetime(
                df["Date"].astype(str) + " " + df["Time"].astype(str),
                format="mixed",
                errors="coerce",
            )
        else:
            raise ValueError("No valid Datetime column found in dataset.")

    df = df.dropna(subset=["Datetime"])
    target_col = resolve_target_column(df)
    df = engineer_features_for_station(df, target_col)
    return df
