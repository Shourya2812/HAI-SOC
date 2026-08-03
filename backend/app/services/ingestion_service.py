"""
backend/app/services/ingestion_service.py

Coordinates the complete log ingestion workflow.
"""

from backend.app.schemas.log_schema import (
    CreateLogRequest,
    LogResponse,
)

from backend.app.services.log_service import LogService
from backend.app.services.anomaly_service import AnomalyService
from backend.app.services.incident_service import IncidentService

from ml.models.predict import Predictor


class IngestionService:
    """
    Orchestrates the complete log ingestion workflow.

    Workflow:

        Client
            │
            ▼
        Validate
            │
            ▼
        Store Log
            │
            ▼
        ML Prediction
            │
            ▼
        Save Prediction
            │
            ▼
        Create Incident (if anomaly)
            │
            ▼
        Return Response
    """

    @staticmethod
    def ingest_log(request: CreateLogRequest):

        # --------------------------------------------------
        # Step 1: Store Log
        # --------------------------------------------------

        created_log: LogResponse = LogService.create_log(request)

        # --------------------------------------------------
        # Step 2: Run ML Prediction
        # --------------------------------------------------

        prediction = Predictor.predict(
            created_log.model_dump()
        )

        # --------------------------------------------------
        # Step 3: Save Prediction
        # --------------------------------------------------

        anomaly_record = AnomalyService.save_prediction(
            log_id=created_log.id,
            detector=prediction["model"],
            prediction=prediction["prediction"],
            anomaly_score=prediction["score"],
        )

        # --------------------------------------------------
        # Step 4: Create Incident (Only if anomaly)
        # --------------------------------------------------

        incident = None

        if prediction["is_anomaly"]:

            incident = IncidentService.create_from_prediction(
                log_id=created_log.id,
                detector=prediction["model"],
                anomaly_score=prediction["score"],
                title="Healthcare Security Anomaly",
                description=(
                    f"An anomalous event was detected by "
                    f"{prediction['model']}."
                ),
            )

        # --------------------------------------------------
        # Step 5: Return Everything
        # --------------------------------------------------

        return {
            "log": created_log,
            "prediction": prediction,
            "anomaly_record": anomaly_record,
            "incident": incident,
        }