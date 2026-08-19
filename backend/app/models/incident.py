"""
backend/app/models/incident.py

Incident model representing a security incident generated
from anomalous healthcare security events.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.enums import (
    IncidentStatus,
    RiskLevel,
)


class Incident(BaseModel):
    """
    Security incident generated after ML anomaly detection.
    """

    # Basic Information
    title: str
    description: str

    # Source Log
    log_id: str

    # ML Information
    detector: str
    anomaly_score: float

    # Classification
    risk_level: RiskLevel
    status: IncidentStatus = IncidentStatus.OPEN

    # Healthcare Context
    hipaa_impact: Optional[str] = None

    # Threat Intelligence
    mitre_technique_id: Optional[str] = None

    # Future AI Report
    report: dict = Field(default_factory=dict)

    # SOC Assignment
    assigned_to: Optional[str] = None

    # Audit Fields
    created_at: datetime
    updated_at: datetime

    resolved_at: Optional[datetime] = None

    model_config = ConfigDict(
        extra="forbid"
    )