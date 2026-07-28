"""
backend/app/api/routes/logs.py

REST endpoints for healthcare security logs.
"""

from fastapi import APIRouter, HTTPException

from backend.app.schemas.log_schema import (
    CreateLogRequest,
    UpdateLogRequest,
    LogResponse,
    IngestionResponse,
)

from backend.app.services.ingestion_service import IngestionService
from backend.app.services.log_service import LogService

from fastapi import Depends
from fastapi import APIRouter, status

from backend.app.api.dependencies import require_role
from backend.app.models.enums import UserRole

router = APIRouter(
    prefix="/logs",
    tags=["Logs"],
)


@router.post(
    "/",
    response_model=IngestionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_log(request: CreateLogRequest):
    return IngestionService.ingest_log(request)

@router.get("/")
def get_logs():
    return LogService.get_logs()


@router.get("/{log_id}")
def get_log(log_id: str):

    log = LogService.get_log(log_id)

    if log is None:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )

    return log


@router.patch(
    "/{log_id}",
    dependencies=[Depends(require_role(UserRole.SOC_ANALYST))]
)
def update_log(
    log_id: str,
    request: UpdateLogRequest,
):

    log = LogService.update_log(
        log_id,
        request,
    )

    if log is None:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )

    return log


@router.delete(
    "/{log_id}",
    dependencies=[Depends(require_role(UserRole.ADMIN))]
)
def delete_log(
    log_id: str,
):

    deleted = LogService.delete_log(log_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Log not found"
        )

    return {
        "message": "Log deleted successfully"
    }