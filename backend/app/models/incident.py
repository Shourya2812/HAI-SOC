from datetime import datetime
from typing import List, Dict, Any

from pydantic import BaseModel
from pydantic import Field


class Incident(BaseModel):
    title: str

    log_ids: List[str]

    risk_level: str

    hipaa_impact: str

    status: str

    mitre_technique_id: str

    report: Dict[str, Any] = Field(default_factory=dict)

    created_at: datetime

    resolved_at: datetime | None = None