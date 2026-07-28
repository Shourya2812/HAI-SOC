"""
Pydantic schemas used by the Log API.
"""

from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field, ConfigDict

from backend.app.models.enums import Severity, Outcome, UserRole


class CreateLogRequest(BaseModel):
    source: str
    destination: Optional[str] = None

    user_id: Optional[str] = None
    role: Optional[UserRole] = None

    device: Optional[str] = None
    department: Optional[str] = None

    action: str

    severity: Severity = Severity.LOW

    protocol: Optional[str] = None
    port: Optional[int] = None

    message: str

    outcome: Outcome

    timestamp: Optional[datetime] = None

    extra: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")

class UpdateLogRequest(BaseModel):
    """
    Request schema for updating an existing log.
    Only mutable fields are allowed.
    """

    severity: Optional[Severity] = None
    message: Optional[str] = None
    outcome: Optional[Outcome] = None
    extra: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="forbid")


class LogResponse(BaseModel):
    """
    Response returned to clients.
    """

    id: str

    timestamp: datetime

    source: str

    destination: Optional[str] = None

    user_id: Optional[str] = None

    role: Optional[UserRole] = None

    device: Optional[str] = None

    department: Optional[str] = None

    action: str

    severity: Severity

    protocol: Optional[str] = None

    port: Optional[int] = None

    message: str

    outcome: Outcome

    extra: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)


class PredictionResponse(BaseModel):
    """
    ML prediction returned for an ingested log.
    """

    model: str
    prediction: int
    is_anomaly: bool
    score: float


class IngestionResponse(BaseModel):
    """
    Response returned after ingesting a log.
    """

    log: LogResponse
    prediction: PredictionResponse