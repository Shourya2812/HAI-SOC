"""
ml/models/one_class_svm.py

Production-grade One-Class SVM pipeline for HAI-SOC.
"""

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import joblib
import pandas as pd
import numpy as np
from sklearn.svm import OneClassSVM

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
logger = logging.getLogger("ocsvm_pipeline")


@dataclass
class OCSVMConfig:
    model_dir: str = "ml/artifacts"
    detector: str = "ocsvm_v1"

    kernel: str = "rbf"
    gamma: str = "scale"

    # Fixed default for production-like behaviour.
    nu: float = 0.10

    test_size: float = 0.20


def train_ocsvm(X_train: np.ndarray,
                config: OCSVMConfig) -> OneClassSVM:

    logger.info(
        f"Training One-Class SVM "
        f"(kernel={config.kernel}, gamma={config.gamma}, nu={config.nu})"
    )

    model = OneClassSVM(
        kernel=config.kernel,
        gamma=config.gamma,
        nu=config.nu,
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

    joblib.dump(model, model_dir / f"{config.detector}.joblib")

    feature_engineer.save(
        model_dir / f"{config.detector}_features.joblib"
    )

    with open(model_dir / f"{config.detector}_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    predictions.to_csv(
        model_dir / f"{config.detector}_predictions.csv",
        index=False
    )

    logger.info(f"Artifacts saved to {model_dir}")


def run_pipeline(config: Optional[OCSVMConfig] = None):

    config = config or OCSVMConfig()

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

    y_test = df_test["label"].values

    model = train_ocsvm(X_train, config)

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
    print(" One-Class SVM RESULTS")
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
