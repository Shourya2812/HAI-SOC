"""
ml/feature_builder.py

Builds ML features from an incoming healthcare log.

This module converts API log objects into the exact feature set
expected by the trained ML models.
"""

from typing import Any

import pandas as pd


class FeatureBuilder:
    """
    Converts a normalized log into the feature set
    expected by the ML models.
    """

    SEVERITY_MAP = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4,
    }

    STATUS_MAP = {
        "SUCCESS": 1,
        "FAILED": 0,
    }

    @staticmethod
    def build(log: dict[str, Any]) -> pd.DataFrame:
        """
        Convert a single log dictionary into the feature
        DataFrame expected by the trained models.
        """

        timestamp = pd.to_datetime(log["timestamp"])

        hour = timestamp.hour
        day_of_week = timestamp.dayofweek
        month = timestamp.month

        is_weekend = int(day_of_week >= 5)
        is_business_hours = int(8 <= hour <= 18)

        severity = str(log.get("severity", "")).upper()

        # Outcome Enum -> SUCCESS / FAILED
        outcome = log.get("outcome")
        if outcome is not None:
            outcome = str(outcome).split(".")[-1].upper()
        else:
            outcome = ""

        extra = log.get("extra", {})

        features = {
            # -------------------------
            # Categorical Features
            # -------------------------
            "source": log.get("source", "UNKNOWN"),
            "event_type": log.get("action", "UNKNOWN"),
            "role": str(log.get("role") or "UNKNOWN"),
            "department": log.get("department") or "UNKNOWN",
            "asset": log.get("device") or "UNKNOWN",
            "protocol": log.get("protocol") or "UNKNOWN",

            # -------------------------
            # Numerical Features
            # -------------------------
            "hour": hour,
            "day_of_week": day_of_week,
            "month": month,
            "is_weekend": is_weekend,
            "is_business_hours": is_business_hours,

            "severity_score": FeatureBuilder.SEVERITY_MAP.get(
                severity,
                0,
            ),

            "status_score": FeatureBuilder.STATUS_MAP.get(
                outcome,
                0,
            ),

            "destination_port": log.get("port") or 0,

            "bytes_sent": extra.get("bytes_sent", 0),
        }

        return pd.DataFrame([features])