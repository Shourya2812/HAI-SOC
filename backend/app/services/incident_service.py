"""
backend/app/services/incident_service.py

Business logic for healthcare security incidents.
"""

from bson import ObjectId

from app.database.collections import incidents_collection

from app.models.incident import Incident

from app.schemas.incident_schema import (
    CreateIncidentRequest,
    UpdateIncidentRequest,
    IncidentResponse,
)


class IncidentService:

    @staticmethod
    def create_incident(request: CreateIncidentRequest) -> IncidentResponse:

        from datetime import datetime, UTC

        incident = Incident(
            title=request.title,
            log_ids=request.log_ids,
            risk_level=request.risk_level,
            hipaa_impact=request.hipaa_impact,
            status="OPEN",
            mitre_technique_id=request.mitre_technique_id,
            report=request.report,
            created_at=datetime.now(UTC),
        )

        result = incidents_collection.insert_one(
            incident.model_dump()
        )

        return IncidentResponse(
            id=str(result.inserted_id),
            **incident.model_dump(),
        )

    @staticmethod
    def get_incident(incident_id: str):

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
    def delete_incident(incident_id: str):

        result = incidents_collection.delete_one(
            {
                "_id": ObjectId(incident_id)
            }
        )

        return result.deleted_count == 1