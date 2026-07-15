from datetime import datetime
from typing import List, Dict, Any

from pydantic import BaseModel, Field, ConfigDict

from app.models.enums import IncidentStatus, RiskLevel


class Incident(BaseModel):
    """
    Security incident generated from anomalous events.
    """

    title: str

    log_ids: List[str]

    risk_level: RiskLevel

    hipaa_impact: str

    status: IncidentStatus

    mitre_technique_id: str

    report: Dict[str, Any] = Field(default_factory=dict)

    created_at: datetime

    resolved_at: datetime | None = None

    model_config = ConfigDict(
        extra="forbid"
    )