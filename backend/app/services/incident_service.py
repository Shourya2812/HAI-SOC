"""
backend/app/services/incident_service.py

Business logic for healthcare security incidents.
"""

from datetime import UTC, datetime

from bson import ObjectId

from backend.app.database.collections import incidents_collection

from backend.app.models.enums import (
    IncidentStatus,
    RiskLevel,
)

from backend.app.models.incident import Incident

from backend.app.schemas.incident_schema import (
    CreateIncidentRequest,
    IncidentResponse,
    UpdateIncidentRequest,
)


class IncidentService:

    # --------------------------------------------------
    # Automatic Incident Creation (Primary Workflow)
    # --------------------------------------------------

    @staticmethod
    def create_from_prediction(
        *,
        log_id: str,
        detector: str,
        anomaly_score: float,
        title: str,
        description: str,
    ) -> IncidentResponse:

        if anomaly_score >= 0.90:
            risk = RiskLevel.CRITICAL

        elif anomaly_score >= 0.75:
            risk = RiskLevel.HIGH

        elif anomaly_score >= 0.50:
            risk = RiskLevel.MEDIUM

        else:
            risk = RiskLevel.LOW

        now = datetime.now(UTC)

        incident = Incident(
            title=title,
            description=description,
            log_id=log_id,
            detector=detector,
            anomaly_score=anomaly_score,
            risk_level=risk,
            status=IncidentStatus.OPEN,
            hipaa_impact=None,
            mitre_technique_id=None,
            report={},
            assigned_to=None,
            created_at=now,
            updated_at=now,
            resolved_at=None,
        )

        result = incidents_collection.insert_one(
            incident.model_dump()
        )

        return IncidentResponse(
            id=str(result.inserted_id),
            **incident.model_dump(),
        )

    # --------------------------------------------------
    # Manual Incident Creation (Optional)
    # --------------------------------------------------

    @staticmethod
    def create_incident(
        request: CreateIncidentRequest,
    ) -> IncidentResponse:

        now = datetime.now(UTC)

        incident = Incident(
            title=request.title,
            description=request.description,
            log_id=request.log_id,
            detector=request.detector,
            anomaly_score=request.anomaly_score,
            risk_level=request.risk_level,
            status=IncidentStatus.OPEN,
            hipaa_impact=request.hipaa_impact,
            mitre_technique_id=request.mitre_technique_id,
            report=request.report,
            assigned_to=request.assigned_to,
            created_at=now,
            updated_at=now,
            resolved_at=None,
        )

        result = incidents_collection.insert_one(
            incident.model_dump()
        )

        return IncidentResponse(
            id=str(result.inserted_id),
            **incident.model_dump(),
        )

    @staticmethod
    def get_incident(
        incident_id: str,
    ):

        document = incidents_collection.find_one(
            {
                "_id": ObjectId(incident_id)
            }
        )

        if document is None:
            return None

        document["id"] = str(document["_id"])

        document.pop("_id")

        return IncidentResponse(**document)

    @staticmethod
    def get_incidents():

        incidents = []

        for document in incidents_collection.find():

            document["id"] = str(document["_id"])

            document.pop("_id")

            incidents.append(
                IncidentResponse(**document)
            )

        return incidents

    @staticmethod
    def update_incident(
        incident_id: str,
        request: UpdateIncidentRequest,
    ):

        update_data = request.model_dump(
            exclude_none=True
        )

        update_data["updated_at"] = datetime.now(UTC)

        incidents_collection.update_one(
            {
                "_id": ObjectId(incident_id)
            },
            {
                "$set": update_data
            }
        )

        return IncidentService.get_incident(
            incident_id
        )

    @staticmethod
    def delete_incident(
        incident_id: str,
    ):

        result = incidents_collection.delete_one(
            {
                "_id": ObjectId(incident_id)
            }
        )

        return result.deleted_count == 1