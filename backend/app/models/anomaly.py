"""
backend/app/models/anomaly.py

Stores every prediction produced by an ML model.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnomalyScore(BaseModel):
    """
    ML prediction associated with a single log.
    """

    log_id: str

    detector: str

    prediction: int

    anomaly_score: float

    created_at: datetime

    model_config = ConfigDict(
        extra="forbid"
    )