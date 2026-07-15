from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field, ConfigDict

from app.models.enums import Severity, Outcome, UserRole


class Log(BaseModel):
    """
    Common schema for healthcare security events.
    """

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

    model_config = ConfigDict(
        extra="forbid"
    )