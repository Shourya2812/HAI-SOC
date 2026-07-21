from datetime import datetime

from app.schemas.canonical_log_schema import CanonicalLog
from app.models.log_enums import (
    LogSource,
    EventSeverity,
    EventStatus,
    UserRole,
)

log = CanonicalLog(
    timestamp=datetime.now(),
    source=LogSource.EHR,
    event_type="VIEW_RECORD",
    user="dr_smith",
    user_role=UserRole.DOCTOR,
    department="Cardiology",
    asset="EHR Server",
    severity=EventSeverity.LOW,
    status=EventStatus.SUCCESS,
    source_ip="10.10.10.5",
    destination_ip="10.10.10.20",
    description="Doctor viewed patient record",
)

print(log.model_dump_json(indent=4))