"""
backend/app/services/anomaly_service.py
"""

from datetime import UTC, datetime

from backend.app.database.collections import anomaly_scores_collection

from backend.app.models.anomaly import AnomalyScore

from backend.app.schemas.anomaly_schema import (
    AnomalyScoreResponse,
)


class AnomalyService:

    @staticmethod
    def save_prediction(
        *,
        log_id: str,
        detector: str,
        prediction: int,
        anomaly_score: float,
    ) -> AnomalyScoreResponse:

        record = AnomalyScore(
            log_id=log_id,
            detector=detector,
            prediction=prediction,
            anomaly_score=anomaly_score,
            created_at=datetime.now(UTC),
        )

        result = anomaly_scores_collection.insert_one(
            record.model_dump()
        )

        return AnomalyScoreResponse(
            id=str(result.inserted_id),
            **record.model_dump(),
        )