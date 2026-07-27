"""
ml/models/xgboost_model.py

Production-grade XGBoost pipeline for HAI-SOC.
Supervised benchmark model.
"""

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import joblib
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
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
logger = logging.getLogger("xgboost_pipeline")


@dataclass
class XGBConfig:
    model_dir: str = "ml/artifacts"
    model_name: str = "xgboost_v1"

    n_estimators: int = 200
    max_depth: int = 5
    learning_rate: float = 0.10
    decision_threshold: float = 0.50
    test_size: float = 0.20


def evaluate_supervised_model(model, X_test, y_test, threshold):
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    metrics = {
        "precision": precision_score(y_test, predictions, zero_division=0),
        "recall": recall_score(y_test, predictions, zero_division=0),
        "f1": f1_score(y_test, predictions, zero_division=0),
        "roc_auc": roc_auc_score(y_test, probabilities),
    }

    cm = confusion_matrix(y_test, predictions)
    tn, fp, fn, tp = cm.ravel()

    metrics["false_positive_rate"] = fp / (fp + tn)
    metrics["confusion_matrix"] = {
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }

    logger.info("Evaluation metrics:\n%s", json.dumps(metrics, indent=2))
    logger.info(
        "\n%s",
        classification_report(
            y_test,
            predictions,
            target_names=["normal", "anomaly"],
            zero_division=0,
        ),
    )

    return metrics, probabilities, predictions


def train_xgboost(X_train, y_train, config):

    positives = max(int(y_train.sum()), 1)
    negatives = len(y_train) - positives
    scale_pos_weight = negatives / positives

    logger.info(
        "Training XGBoost "
        f"(estimators={config.n_estimators}, "
        f"depth={config.max_depth}, "
        f"scale_pos_weight={scale_pos_weight:.2f})"
    )

    model = XGBClassifier(
        n_estimators=config.n_estimators,
        max_depth=config.max_depth,
        learning_rate=config.learning_rate,
        scale_pos_weight=scale_pos_weight,
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    return model


def save_artifacts(model, fe, metrics, predictions, config):
    model_dir = Path(config.model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_dir / f"{config.model_name}.joblib")
    fe.save(model_dir / f"{config.model_name}_features.joblib")

    with open(model_dir / f"{config.model_name}_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    predictions.to_csv(
        model_dir / f"{config.model_name}_predictions.csv",
        index=False,
    )

    logger.info("Artifacts saved to %s", model_dir)


def run_pipeline(config: Optional[XGBConfig] = None):

    config = config or XGBConfig()

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

    y_train = df_train["label"].values
    y_test = df_test["label"].values

    model = train_xgboost(X_train, y_train, config)

    metrics, probabilities, predictions = evaluate_supervised_model(
        model,
        X_test,
        y_test,
        config.decision_threshold,
    )

    metrics["per_attack_type_recall"] = evaluate_per_attack_type(
        df_test,
        predictions,
    )

    print("\n==========================")
    print(" XGBOOST RESULTS")
    print("==========================")
    print(f"Precision : {metrics['precision']:.4f}")
    print(f"Recall    : {metrics['recall']:.4f}")
    print(f"F1 Score  : {metrics['f1']:.4f}")
    print(f"ROC-AUC   : {metrics['roc_auc']:.4f}")
    print("==========================\n")

    pred_df = pd.DataFrame({
        "timestamp": df_test["timestamp"],
        "attack_type": df_test["attack_type"],
        "label": y_test,
        "prediction": predictions,
        "probability": probabilities,
    })

    save_artifacts(
        model,
        fe,
        metrics,
        pred_df,
        config,
    )

    return model, fe, metrics


if __name__ == "__main__":
    run_pipeline()
