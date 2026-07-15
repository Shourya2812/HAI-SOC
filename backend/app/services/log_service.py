"""
backend/app/services/log_service.py

Business logic for healthcare security logs.
"""

from datetime import datetime, UTC

from bson import ObjectId

from app.database.collections import logs_collection

from app.models.enums import Severity

from app.models.log import Log

from app.schemas.log_schema import (
    CreateLogRequest,
    UpdateLogRequest,
    LogResponse,
)


class LogService:

    @staticmethod
    def create_log(request: CreateLogRequest) -> LogResponse:
        """
        Create a new healthcare security log.
        """

        log = Log(
            timestamp=datetime.now(UTC),
            source=request.source,
            destination=request.destination,
            user_id=request.user_id,
            role=request.role,
            device=request.device,
            department=request.department,
            action=request.action,
            severity=Severity.LOW,
            protocol=request.protocol,
            port=request.port,
            message=request.message,
            outcome=request.outcome,
            extra=request.extra,
        )

        result = logs_collection.insert_one(log.model_dump())

        return LogResponse(
            id=str(result.inserted_id),
            **log.model_dump(),
        )

    @staticmethod
    def get_log(log_id: str):

        document = logs_collection.find_one(
            {
                "_id": ObjectId(log_id)
            }
        )

        if document is None:
            return None

        document["id"] = str(document["_id"])

        document.pop("_id")

        return LogResponse(**document)

    @staticmethod
    def get_logs():

        logs = []

        for document in logs_collection.find():

            document["id"] = str(document["_id"])

            document.pop("_id")

            logs.append(
                LogResponse(**document)
            )

        return logs

    @staticmethod
    def delete_log(log_id: str):

        result = logs_collection.delete_one(
            {
                "_id": ObjectId(log_id)
            }
        )

        return result.deleted_count == 1

    @staticmethod
    def update_log(log_id: str, request: UpdateLogRequest):

        update_data = request.model_dump(
            exclude_none=True
        )

        logs_collection.update_one(
            {
                "_id": ObjectId(log_id)
            },
            {
                "$set": update_data
            }
        )

        return LogService.get_log(log_id)