"""
backend/app/api/routes/incidents.py

REST endpoints for healthcare security incidents.
"""

from fastapi import APIRouter, HTTPException

from app.schemas.incident_schema import (
    CreateIncidentRequest,
    UpdateIncidentRequest,
)

from app.services.incident_service import IncidentService

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


@router.post("/")
def create_incident(request: CreateIncidentRequest):
    return IncidentService.create_incident(request)


@router.get("/")
def get_incidents():
    return IncidentService.get_incidents()


@router.get("/{incident_id}")
def get_incident(incident_id: str):

    incident = IncidentService.get_incident(
        incident_id
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident


@router.patch("/{incident_id}")
def update_incident(
    incident_id: str,
    request: UpdateIncidentRequest,
):

    incident = IncidentService.update_incident(
        incident_id,
        request,
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident


@router.delete("/{incident_id}")
def delete_incident(
    incident_id: str,
):

    deleted = IncidentService.delete_incident(
        incident_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return {
        "message": "Incident deleted successfully"
    }