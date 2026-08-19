"""
backend/app/api/routes/incidents.py

REST endpoints for healthcare security incidents.
"""

from fastapi import APIRouter, Depends, HTTPException

from backend.app.api.dependencies import require_role
from backend.app.models.enums import UserRole
from backend.app.schemas.incident_schema import (
    CreateIncidentRequest,
    IncidentResponse,
    UpdateIncidentRequest,
)
from backend.app.services.incident_service import IncidentService

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


@router.post(
    "/",
    response_model=IncidentResponse,
    dependencies=[Depends(require_role(UserRole.SOC_ANALYST))],
)
def create_incident(request: CreateIncidentRequest):
    return IncidentService.create_incident(request)


@router.get(
    "/",
    response_model=list[IncidentResponse],
)
def get_incidents():
    return IncidentService.get_incidents()


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
)
def get_incident(incident_id: str):
    incident = IncidentService.get_incident(incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    return incident


@router.patch(
    "/{incident_id}",
    response_model=IncidentResponse,
)
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
            detail="Incident not found",
        )

    return incident


@router.delete(
    "/{incident_id}",
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)
def delete_incident(
    incident_id: str,
):
    deleted = IncidentService.delete_incident(
        incident_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    return {
        "message": "Incident deleted successfully"
    }


@router.post(
    "/{incident_id}/analyze",
    response_model=IncidentResponse,
)
def analyze_incident_endpoint(
    incident_id: str,
):
    """
    Trigger on-demand grounded RAG analysis for a security incident.
    Generates and persists the AI investigation report in MongoDB.
    """
    try:
        updated_incident = IncidentService.generate_incident_report(incident_id)
        if updated_incident is None:
            raise HTTPException(
                status_code=404,
                detail="Incident not found",
            )
        return updated_incident
    except ValueError as val_err:
        err_msg = str(val_err)
        if "not found" in err_msg.lower() or "invalid" in err_msg.lower():
            raise HTTPException(status_code=404, detail=err_msg)
        raise HTTPException(status_code=400, detail=err_msg)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate AI investigation report. Please try again.",
        )