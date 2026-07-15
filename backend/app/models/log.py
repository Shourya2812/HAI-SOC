from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class Log(BaseModel):
    timestamp: datetime

    source: str

    destination: Optional[str] = None

    user_id: Optional[str] = None

    role: Optional[str] = None

    device: Optional[str] = None

    department: Optional[str] = None

    action: str

    severity: str

    protocol: Optional[str] = None

    port: Optional[int] = None

    message: str

    outcome: str

    extra: Dict[str, Any] = Field(default_factory=dict)