import os
from typing import Any, Dict, List, Optional, Tuple, Union

import joblib
import numpy as np
import pandas as pd

from .feature_columns import build_manual_feature_vector
from .train import train_and_save_bundle

_bundle: Optional[Dict[str, Any]] = None


def _backend_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _bundle_path() -> str:
    return os.path.join(_backend_dir(), "models", "model_bundle.joblib")


def ensure_model_trained() -> None:
    """Train (or retrain) if bundle missing."""
    if not os.path.isfile(_bundle_path()):
        print("Model bundle not found. Training from data/ ...")
        train_and_save_bundle(_backend_dir(), force_refresh_data=False)


def load_bundle() -> Dict[str, Any]:
    global _bundle
    if _bundle is not None:
        return _bundle

    ensure_model_trained()
    _bundle = joblib.load(_bundle_path())
    return _bundle


def load_model():
    """
    Backwards-compatible: returns (estimator, scaler) tuple.
    Estimator is WeightedEnsemble with .predict.
    """
    b = load_bundle()
    return b["estimator"], b["scaler"]


def get_feature_columns() -> List[str]:
    b = load_bundle()
    return list(b["feature_columns"])


def get_defaults() -> Dict[str, float]:
    b = load_bundle()
    return dict(b.get("defaults", {}))


def predict_single(features: dict) -> float:
    b = load_bundle()
    model = b["estimator"]
    scaler = b["scaler"]
    columns: List[str] = b["feature_columns"]
    defaults: Dict[str, float] = b.get("defaults", {})

    row = build_manual_feature_vector(features, defaults, columns)
    X = pd.DataFrame([row], columns=columns)
    if scaler is not None:
        X = scaler.transform(X)
    else:
        X = X.to_numpy(dtype=float)
    return float(model.predict(X)[0])


def predict_batch(X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
    b = load_bundle()
    model = b["estimator"]
    scaler = b["scaler"]
    cols: List[str] = b["feature_columns"]
    if isinstance(X, np.ndarray):
        X = pd.DataFrame(X, columns=cols)
    if scaler is not None:
        X = scaler.transform(X)
    elif hasattr(X, "to_numpy"):
        X = X.to_numpy(dtype=float)
    return model.predict(X)


def auto_generate_model(base_dir: str) -> None:
    """Used if legacy code paths call this; trains full bundle from all data files."""
    train_and_save_bundle(base_dir, force_refresh_data=True)
