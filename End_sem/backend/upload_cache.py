"""
TTL disk cache for batch upload results (default 2 hours).
Speeds up repeat uploads of the same file and restores processed DataFrame for the agent.
"""

from __future__ import annotations

import json
import os
import time
import hashlib
from typing import Any, Dict, Optional

import joblib
import pandas as pd

# 2 hours
DEFAULT_TTL_SECONDS = 7200


def _cache_root() -> str:
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "cache", "uploads")


def _ensure_dir() -> str:
    p = _cache_root()
    os.makedirs(p, exist_ok=True)
    return p


def make_cache_key(filename: str, contents: bytes) -> str:
    h = hashlib.sha256()
    h.update((filename or "upload").encode("utf-8", errors="ignore"))
    h.update(b"|")
    h.update(str(len(contents)).encode())
    h.update(b"|")
    h.update(contents)
    return h.hexdigest()


def _meta_path(key: str) -> str:
    return os.path.join(_cache_root(), f"{key}.meta.json")


def _df_path(key: str) -> str:
    return os.path.join(_cache_root(), f"{key}.df.joblib")


def prune_expired() -> None:
    """Remove expired cache entries (best-effort)."""
    root = _cache_root()
    if not os.path.isdir(root):
        return
    now = time.time()
    for name in os.listdir(root):
        if not name.endswith(".meta.json"):
            continue
        mp = os.path.join(root, name)
        try:
            with open(mp, "r", encoding="utf-8") as f:
                meta = json.load(f)
            if now > float(meta.get("expires_at", 0)):
                key = name.replace(".meta.json", "")
                for path in (_meta_path(key), _df_path(key)):
                    if os.path.isfile(path):
                        os.remove(path)
        except (OSError, json.JSONDecodeError, KeyError):
            continue


def get_cached_batch(key: str) -> Optional[Dict[str, Any]]:
    """Returns { 'response_data': dict, 'df': DataFrame } or None."""
    prune_expired()
    mp, dp = _meta_path(key), _df_path(key)
    if not os.path.isfile(mp) or not os.path.isfile(dp):
        return None
    try:
        with open(mp, "r", encoding="utf-8") as f:
            meta = json.load(f)
        if time.time() > float(meta["expires_at"]):
            for path in (mp, dp):
                if os.path.isfile(path):
                    os.remove(path)
            return None
        df: pd.DataFrame = joblib.load(dp)
        return {"response_data": meta["response_data"], "df": df}
    except Exception:
        return None


def store_batch_cache(
    key: str,
    response_data: Dict[str, Any],
    processed_df: pd.DataFrame,
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
) -> None:
    _ensure_dir()
    expires_at = time.time() + ttl_seconds
    meta = {
        "expires_at": expires_at,
        "response_data": response_data,
        "cached_at": time.time(),
        "ttl_seconds": ttl_seconds,
    }
    with open(_meta_path(key), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    joblib.dump(processed_df, _df_path(key), compress=3)
