from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import Severity


class Anomaly(BaseModel):
    """
    ML anomaly score for a healthcare log.
    """

    log_id: str

    anomaly_score: float

    risk_score: float

    confidence: float

    severity: Severity

    model_name: str

    model_version: str

    scored_at: datetime

    model_config = ConfigDict(
        extra="forbid"
    )