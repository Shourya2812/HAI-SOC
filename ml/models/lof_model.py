"""
ml/models/local_outlier_factor.py

Production-grade Local Outlier Factor pipeline for HAI-SOC.

Changes:
- Reuses FeatureEngineer, dataset loading, evaluation and train/test split.
- Uses project dataset path from ml.config through IForestConfig.
- Supports novelty=True for inference.
- Saves model, preprocessing artifacts, metrics and predictions.
"""

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import joblib
import pandas as pd
import numpy as np
from sklearn.neighbors import LocalOutlierFactor

from ml.models.isolation_forest import (
    IForestConfig,
    FeatureEngineer,
    load_dataset,
    train_test_split_chronological,
    evaluate_model,
    evaluate_per_attack_type,
)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("lof_pipeline")


@dataclass
class LOFConfig:
    model_dir: str = "ml/artifacts"
    model_name: str = "lof_v1"

    n_neighbors: int = 20
    contamination: Optional[float] = 0.10
    test_size: float = 0.20


def train_lof(X_train: np.ndarray,
              config: LOFConfig) -> LocalOutlierFactor:

    logger.info(
        f"Training LOF (n_neighbors={config.n_neighbors}, "
        f"contamination={config.contamination:.3f})"
    )

    model = LocalOutlierFactor(
        n_neighbors=config.n_neighbors,
        contamination=config.contamination,
        novelty=True,
        n_jobs=-1,
    )

    model.fit(X_train)
    return model


def save_artifacts(model,
                   feature_engineer,
                   metrics,
                   predictions,
                   config):

    model_dir = Path(config.model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_dir / f"{config.model_name}.joblib")

    feature_engineer.save(
        model_dir / f"{config.model_name}_features.joblib"
    )

    with open(model_dir / f"{config.model_name}_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    predictions.to_csv(
        model_dir / f"{config.model_name}_predictions.csv",
        index=False
    )

    logger.info(f"Artifacts saved to {model_dir}")


def run_pipeline(config: Optional[LOFConfig] = None):

    config = config or LOFConfig()

    # Uses dataset path and feature definitions from Isolation Forest config.
    fe_config = IForestConfig()

    df = load_dataset(fe_config)

    df_train, df_test = train_test_split_chronological(
        df,
        config.test_size
    )

    logger.info(
        f"Train: {len(df_train)} rows | Test: {len(df_test)} rows"
    )

    fe = FeatureEngineer(fe_config)

    X_train = fe.fit_transform(df_train)
    X_test = fe.transform(df_test)

    y_train = df_train["label"].values
    y_test = df_test["label"].values

    model = train_lof(X_train, config)

    metrics, scores, preds = evaluate_model(
        model,
        X_test,
        y_test
    )

    metrics["per_attack_type_recall"] = evaluate_per_attack_type(
        df_test,
        preds
    )

    print("\n==========================")
    print(" LOF RESULTS")
    print("==========================")
    print(f"Precision : {metrics['precision']:.4f}")
    print(f"Recall    : {metrics['recall']:.4f}")
    print(f"F1 Score  : {metrics['f1']:.4f}")
    print(f"ROC-AUC   : {metrics['roc_auc']:.4f}")
    print("==========================\n")

    predictions = pd.DataFrame({
        "timestamp": df_test["timestamp"],
        "attack_type": df_test["attack_type"],
        "label": y_test,
        "prediction": preds,
        "anomaly_score": scores,
    })

    save_artifacts(
        model,
        fe,
        metrics,
        predictions,
        config,
    )

    return model, fe, metrics


if __name__ == "__main__":
    run_pipeline()
