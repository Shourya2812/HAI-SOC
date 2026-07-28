"""
backend/app/services/ingestion_service.py

Coordinates the complete log ingestion workflow.
This service orchestrates log persistence, ML prediction,
and incident generation.
"""

from backend.app.schemas.log_schema import (
    CreateLogRequest,
    LogResponse,
    PredictionResponse,
    IngestionResponse,
)

from backend.app.services.log_service import LogService
from ml.models.predict import Predictor


class IngestionService:
    """
    Orchestrates the end-to-end ingestion pipeline.
    """

    @staticmethod
    def ingest_log(request: CreateLogRequest) -> IngestionResponse:
        """
        Main entry point for log ingestion.

        Workflow:
            Client
                ↓
            Validate (Pydantic)
                ↓
            Store Log
                ↓
            Build Features
                ↓
            ML Prediction
                ↓
            Return Response
        """

        # Save log to MongoDB
        created_log = LogService.create_log(request)

        # Run ML prediction
        prediction = Predictor.predict(
            created_log.model_dump()
        )

        return IngestionResponse(
            log=created_log,
            prediction=PredictionResponse(**prediction),
        )

    @staticmethod
    def run_ml_pipeline(log: LogResponse):
        """
        Placeholder for ML prediction.

        Future implementation:
            - Feature Engineering
            - Load trained model
            - Predict anomaly score
            - Store prediction
        """
        raise NotImplementedError("ML pipeline not implemented yet.")

    @staticmethod
    def create_incident_if_needed(
        log: LogResponse,
        prediction: PredictionResponse,
    ):
        """
        Placeholder for automatic incident creation.

        Future implementation:
            - Compare anomaly score with threshold
            - Create incident
            - Store incident
            - Notify SOC
        """
        raise NotImplementedError("Incident creation not implemented yet.")