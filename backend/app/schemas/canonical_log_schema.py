from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, ConfigDict

from app.models.log_enums import (
    EventSeverity,
    EventStatus,
    LogSource,
    UserRole,
)


class CanonicalLog(BaseModel):
    """
    Standardized healthcare security log.
    Every log source must be converted into this format.
    """

    timestamp: datetime

    source: LogSource

    event_type: str

    user: str

    user_role: UserRole

    department: str | None = None

    asset: str

    severity: EventSeverity

    status: EventStatus

    source_ip: str

    destination_ip: str

    description: str

    extra: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")