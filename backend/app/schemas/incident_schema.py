"""
backend/app/schemas/incident_schema.py

Pydantic schemas used by the Incident API.
"""

from datetime import datetime
from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.enums import (
    IncidentStatus,
    RiskLevel,
)


class IncidentReportSchema(BaseModel):
    """
    Structured AI investigation report schema.
    """

    raw_markdown: str = ""
    generated_at: Optional[datetime] = None
    mitre_techniques: list[str] = Field(default_factory=list)
    nist_controls: list[str] = Field(default_factory=list)
    hipaa_impact: Optional[str] = None
    risk_assessment: Optional[str] = None
    recommended_actions: list[str] = Field(default_factory=list)
    status: str = "GENERATED"

    model_config = ConfigDict(extra="allow")


class CreateIncidentRequest(BaseModel):
    """
    Manual incident creation.

    Normally incidents will be created automatically
    by the ML pipeline, but SOC analysts can also
    create incidents manually.
    """

    title: str

    description: str

    log_id: str

    detector: str

    anomaly_score: float

    risk_level: RiskLevel

    hipaa_impact: Optional[str] = None

    mitre_technique_id: Optional[str] = None

    report: Union[IncidentReportSchema, dict[str, Any]] = Field(default_factory=dict)

    assigned_to: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class UpdateIncidentRequest(BaseModel):
    """
    Update an existing incident.
    """

    status: Optional[IncidentStatus] = None

    risk_level: Optional[RiskLevel] = None

    assigned_to: Optional[str] = None

    report: Optional[Union[IncidentReportSchema, dict[str, Any]]] = None

    resolved_at: Optional[datetime] = None

    model_config = ConfigDict(extra="forbid")


class IncidentResponse(BaseModel):
    """
    Response returned to API clients.
    """

    id: str

    title: str

    description: str

    log_id: str

    detector: str

    anomaly_score: float

    risk_level: RiskLevel

    status: IncidentStatus

    hipaa_impact: Optional[str] = None

    mitre_technique_id: Optional[str] = None

    report: Union[IncidentReportSchema, dict[str, Any]] = Field(default_factory=dict)

    assigned_to: Optional[str] = None

    created_at: datetime

    updated_at: datetime

    resolved_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)