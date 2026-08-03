"""
backend/app/schemas/anomaly_schema.py
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnomalyScoreResponse(BaseModel):

    id: str

    log_id: str

    detector: str

    prediction: int

    anomaly_score: float

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)