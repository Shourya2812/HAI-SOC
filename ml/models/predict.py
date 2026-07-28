"""
ml/models/predict.py

Inference service for HAI-SOC.
"""

from typing import Any

from ml.feature_builder import FeatureBuilder
from ml.models.model_loader import ModelLoader

DEFAULT_MODEL = "xgboost_v1"


class Predictor:

    @staticmethod
    def predict(log: dict[str, Any]) -> dict:

        model, feature_engineer = ModelLoader.load_model(DEFAULT_MODEL)

        # Build inference features
        feature_df = FeatureBuilder.build(log)

        # Encode + Scale
        X = feature_engineer.transform(feature_df)

        # Predict
        probability = float(model.predict_proba(X)[0][1])

        prediction = int(probability >= 0.50)

        return {
            "model": DEFAULT_MODEL,
            "prediction": prediction,
            "is_anomaly": bool(prediction),
            "score": round(probability, 4),
        }