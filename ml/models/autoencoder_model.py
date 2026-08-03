"""
ml/models/autoencoder_model.py

Production-grade AutoEncoder pipeline for HAI-SOC.
Uses the same preprocessing pipeline as the other models and saves
model, preprocessing artifacts, metrics, and predictions.
"""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import joblib
import numpy as np
import pandas as pd
from pyod.models.auto_encoder import AutoEncoder
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

from ml.models.isolation_forest import (
    IForestConfig,
    FeatureEngineer,
    load_dataset,
    train_test_split_chronological,
    evaluate_per_attack_type,
)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("autoencoder_pipeline")


@dataclass
class AutoEncoderConfig:
    model_dir: str = "ml/artifacts"
    detector: str = "autoencoder_v1"

    hidden_neuron_list: list = field(default_factory=lambda: [8, 4, 4, 8])
    epochs: int = 50
    batch_size: int = 32

    # Fixed default instead of inferring from labels
    contamination: float = 0.10

    test_size: float = 0.20


def evaluate_pyod_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    anomaly_scores = model.decision_function(X_test)

    metrics = {
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, anomaly_scores),
    }

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    metrics["false_positive_rate"] = fp / (fp + tn)
    metrics["confusion_matrix"] = {
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }

    logger.info("Evaluation metrics:\n%s",
                json.dumps(metrics, indent=2))
    logger.info("\n%s",
                classification_report(
                    y_test,
                    y_pred,
                    target_names=["normal", "anomaly"],
                    zero_division=0,
                ))

    return metrics, anomaly_scores, y_pred


def train_autoencoder(X_train, config):
    logger.info(
        "Training AutoEncoder "
        f"(layers={config.hidden_neuron_list}, "
        f"epochs={config.epochs}, "
        f"contamination={config.contamination})"
    )

    model = AutoEncoder(
        hidden_neuron_list=config.hidden_neuron_list,
        epoch_num=config.epochs,
        batch_size=config.batch_size,
        contamination=config.contamination,
    )

    model.fit(X_train)
    return model


def save_artifacts(model, fe, metrics, predictions, config):
    model_dir = Path(config.model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_dir / f"{config.detector}.joblib")
    fe.save(model_dir / f"{config.detector}_features.joblib")

    with open(model_dir / f"{config.detector}_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    predictions.to_csv(
        model_dir / f"{config.detector}_predictions.csv",
        index=False,
    )

    logger.info("Artifacts saved to %s", model_dir)


def run_pipeline(config: Optional[AutoEncoderConfig] = None):
    config = config or AutoEncoderConfig()

    fe_config = IForestConfig()

    df = load_dataset(fe_config)

    df_train, df_test = train_test_split_chronological(
        df,
        config.test_size,
    )

    logger.info(
        "Train: %d rows | Test: %d rows",
        len(df_train),
        len(df_test),
    )

    fe = FeatureEngineer(fe_config)

    X_train = fe.fit_transform(df_train)
    X_test = fe.transform(df_test)

    y_test = df_test["label"].values

    model = train_autoencoder(X_train, config)

    metrics, scores, preds = evaluate_pyod_model(
        model,
        X_test,
        y_test,
    )

    metrics["per_attack_type_recall"] = evaluate_per_attack_type(
        df_test,
        preds,
    )

    print("\n==========================")
    print(" AUTOENCODER RESULTS")
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
