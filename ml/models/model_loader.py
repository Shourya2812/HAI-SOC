"""
ml/models/model_loader.py

Loads trained ML models and their corresponding preprocessing
artifacts for inference.
"""

from pathlib import Path
from ml.models.isolation_forest import FeatureEngineer
import joblib


ARTIFACTS_DIR = Path("ml/artifacts")


class ModelLoader:
    """
    Singleton-style loader for ML models.

    Models and feature engineering artifacts are loaded only once
    and then reused throughout the application.
    """

    _cache = {}

    @classmethod
    def load_model(cls, model_name: str):
        """
        Load a trained model and its feature engineering artifacts.

        Args:
            model_name:
                Example:
                    xgboost_v1
                    isolation_forest_v1
                    lof_v1
                    ocsvm_v1
                    autoencoder_v1

        Returns:
            tuple:
                (model, feature_engineer)
        """

        if model_name not in cls._cache:

            model_path = ARTIFACTS_DIR / f"{model_name}.joblib"
            feature_path = ARTIFACTS_DIR / f"{model_name}_features.joblib"

            model = joblib.load(model_path)
            feature_engineer = FeatureEngineer.load(feature_path)

            cls._cache[model_name] = (
                model,
                feature_engineer,
            )

        return cls._cache[model_name]

    @classmethod
    def clear_cache(cls):
        """
        Clear all loaded models.
        Useful during development/testing.
        """
        cls._cache.clear()