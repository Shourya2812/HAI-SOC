"""
Pydantic schemas used by the Incident API.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional

from pydantic import BaseModel, Field, ConfigDict

from app.models.enums import IncidentStatus, RiskLevel


class CreateIncidentRequest(BaseModel):
    title: str
    description: str
    risk_level: RiskLevel


class UpdateIncidentRequest(BaseModel):
    """
    Request schema for updating an incident.
    """

    status: Optional[IncidentStatus] = None

    risk_level: Optional[RiskLevel] = None

    report: Optional[Dict[str, Any]] = None

    resolved_at: Optional[datetime] = None

    model_config = ConfigDict(extra="forbid")


class IncidentResponse(BaseModel):
    """
    Response schema returned to clients.
    """

    id: str

    title: str

    log_ids: List[str]

    risk_level: RiskLevel

    hipaa_impact: str

    status: IncidentStatus

    mitre_technique_id: str

    report: Dict[str, Any] = Field(default_factory=dict)

    created_at: datetime

    resolved_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)