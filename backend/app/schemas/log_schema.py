"""
Pydantic schemas used by the Log API.
"""

from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field, ConfigDict

from app.models.enums import Severity, Outcome, UserRole


class CreateLogRequest(BaseModel):
    """
    Request schema for creating a new healthcare security log.
    """

    source: str
    destination: Optional[str] = None
    user_id: Optional[str] = None
    role: Optional[UserRole] = None
    device: Optional[str] = None
    department: Optional[str] = None
    action: str
    protocol: Optional[str] = None
    port: Optional[int] = None
    message: str
    outcome: Outcome
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