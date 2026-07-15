from datetime import datetime

from pydantic import BaseModel


class Anomaly(BaseModel):
    log_id: str

    anomaly_score: float

    risk_score: float

    confidence: float

    severity: str

    model_name: str

    model_version: str

    scored_at: datetime