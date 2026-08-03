"""
ml/training/train_isolation_forest.py

Production-grade Isolation Forest training pipeline for HAI-SOC.

Pipeline stages:
  1. Load ml_dataset.csv (from attack_injector.py)
  2. Feature engineering (encode categoricals, derive time features, scale)
  3. Train Isolation Forest (unsupervised — trained WITHOUT labels)
  4. Evaluate against ground-truth labels (precision, recall, F1, ROC-AUC, FPR)
  5. Persist model + preprocessing artifacts for reuse in inference/API

Run: python -m ml.training.train_isolation_forest
"""

import json
import logging
from dataclasses import field
from dataclasses import dataclass
from ml.config import ML_DATASET
from pathlib import Path
from typing import Optional

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("iforest_pipeline")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

@dataclass
class IForestConfig:
    data_path: str = str(ML_DATASET)
    model_dir: str = "ml/artifacts"
    detector: str = "isolation_forest_v1"

    categorical_cols: list = field(default_factory=lambda: [
        "source", "event_type", "role", "department", "asset", "protocol",
    ])
    numeric_cols: list = field(default_factory=lambda: [
        "hour",
        "day_of_week",
        "month",
        "is_weekend",
        "is_business_hours",
        "severity_score",
        "status_score",
        "destination_port",
        "bytes_sent",
    ])

    # Isolation Forest hyperparameters
    n_estimators: int = 200
    max_samples: str = "auto"
    contamination: Optional[float] = None  # if None, inferred from training data label rate
    random_state: int = 42

    test_size: float = 0.2


# ---------------------------------------------------------------------------
# Feature engineering
# ---------------------------------------------------------------------------

class FeatureEngineer:
    """Encapsulates all preprocessing so the exact same transforms can be
    replayed at inference time. Fit on train, reused (never refit) on test/prod."""

    def __init__(self, config: IForestConfig):
        self.config = config
        self.label_encoders: dict[str, LabelEncoder] = {}
        self.scaler: Optional[StandardScaler] = None
        self.feature_names: list[str] = []

    @staticmethod
    def _derive_time_features(df: pd.DataFrame) -> pd.DataFrame:
        """
        Dataset already contains engineered time features.
        No additional timestamp parsing is required.
        """
        return df.copy()

    def fit_transform(self, df: pd.DataFrame) -> np.ndarray:
        df = self._derive_time_features(df)

        for col in self.config.categorical_cols:
            le = LabelEncoder()
            df[col] = df[col].astype(str).fillna("UNKNOWN")
            df[col + "_enc"] = le.fit_transform(df[col])
            self.label_encoders[col] = le

        encoded_cat_cols = [c + "_enc" for c in self.config.categorical_cols]
        self.feature_names = encoded_cat_cols + self.config.numeric_cols

        X = df[self.feature_names].fillna(0).values
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        df = self._derive_time_features(df)

        for col in self.config.categorical_cols:
            le = self.label_encoders[col]
            df[col] = df[col].astype(str).fillna("UNKNOWN")
            # unseen categories at inference time -> map to a fixed "unknown" bucket
            df[col + "_enc"] = df[col].apply(
                lambda v: le.transform([v])[0] if v in le.classes_ else -1
            )

        X = df[self.feature_names].fillna(0).values
        return self.scaler.transform(X)

    def save(self, path: Path):
        joblib.dump(
            {
                "label_encoders": self.label_encoders,
                "scaler": self.scaler,
                "feature_names": self.feature_names,
                "config": self.config,
            },
            path,
        )

    @classmethod
    def load(cls, path: Path) -> "FeatureEngineer":
        payload = joblib.load(path)
        fe = cls(payload["config"])
        fe.label_encoders = payload["label_encoders"]
        fe.scaler = payload["scaler"]
        fe.feature_names = payload["feature_names"]
        return fe


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_dataset(config: IForestConfig) -> pd.DataFrame:
    path = Path(config.data_path)
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found — run datasets/generators/attack_injector.py first."
        )
    df = pd.read_csv(path)
    logger.info(f"Loaded {len(df)} rows from {path}")
    return df


def train_test_split_chronological(df: pd.DataFrame, test_size: float):
    """Chronological split, not random — a SOC model should be validated on
    events *after* the training window, mirroring how it'll be used in production."""
    df = df.sort_values("timestamp").reset_index(drop=True)
    split_idx = int(len(df) * (1 - test_size))
    return df.iloc[:split_idx].reset_index(drop=True), df.iloc[split_idx:].reset_index(drop=True)


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

def train_model(X_train: np.ndarray, config: IForestConfig, contamination: float) -> IsolationForest:
    logger.info(
        f"Training Isolation Forest (n_estimators={config.n_estimators}, "
        f"contamination={contamination:.4f})"
    )
    model = IsolationForest(
        n_estimators=config.n_estimators,
        max_samples=config.max_samples,
        contamination=contamination,
        random_state=config.random_state,
        n_jobs=-1,
    )
    model.fit(X_train)
    return model


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def evaluate_model(model: IsolationForest, X_test: np.ndarray, y_test: np.ndarray) -> dict:
    # IsolationForest.predict returns 1 (normal) / -1 (anomaly) — remap to 0/1
    raw_preds = model.predict(X_test)
    y_pred = np.where(raw_preds == -1, 1, 0)

    # decision_function: higher = more normal. Flip sign so higher = more anomalous,
    # which is the convention we want for ROC-AUC against label=1 (attack).
    anomaly_scores = -model.decision_function(X_test)

    metrics = {
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, anomaly_scores) if len(set(y_test)) > 1 else float("nan"),
    }

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)
    metrics["false_positive_rate"] = fp / (fp + tn) if (fp + tn) > 0 else float("nan")
    metrics["confusion_matrix"] = {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}

    logger.info("Evaluation metrics:\n" + json.dumps(metrics, indent=2, default=str))
    logger.info("\n" + classification_report(y_test, y_pred, target_names=["normal", "anomaly"], zero_division=0))

    return metrics, anomaly_scores, y_pred


def evaluate_per_attack_type(df_test: pd.DataFrame, y_pred: np.ndarray) -> dict:
    """Breaks down recall per attack type — critical because a single blended
    F1 score hides whether the model is actually catching insider threats
    (hard) vs. only catching brute force (easy)."""
    df_test = df_test.copy()
    df_test["pred"] = y_pred
    breakdown = {}
    for attack_type in df_test.loc[df_test["label"] == 1, "attack_type"].unique():
        subset = df_test[df_test["attack_type"] == attack_type]
        recall = (subset["pred"] == 1).mean()
        breakdown[attack_type] = {"count": len(subset), "recall": round(float(recall), 4)}
    logger.info("Per-attack-type recall:\n" + json.dumps(breakdown, indent=2))
    return breakdown


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def save_artifacts(model: IsolationForest, feature_engineer: FeatureEngineer,
                    metrics: dict, config: IForestConfig):
    model_dir = Path(config.model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_dir / f"{config.detector}.joblib")
    feature_engineer.save(model_dir / f"{config.detector}_features.joblib")

    with open(model_dir / f"{config.detector}_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2, default=str)

    logger.info(f"Artifacts saved to {model_dir}/")


def load_artifacts(config: IForestConfig):
    model_dir = Path(config.model_dir)
    model = joblib.load(model_dir / f"{config.detector}.joblib")
    feature_engineer = FeatureEngineer.load(model_dir / f"{config.detector}_features.joblib")
    return model, feature_engineer


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_pipeline(config: Optional[IForestConfig] = None):
    config = config or IForestConfig()

    df = load_dataset(config)
    df_train, df_test = train_test_split_chronological(df, config.test_size)
    logger.info(f"Train: {len(df_train)} rows | Test: {len(df_test)} rows")

    fe = FeatureEngineer(config)
    X_train = fe.fit_transform(df_train)
    X_test = fe.transform(df_test)

    y_train = df_train["label"].values
    y_test = df_test["label"].values

    # Contamination = expected fraction of anomalies. In production you
    # wouldn't have labels at all, but since this is a labeled synthetic
    # dataset we can use the training label rate as a realistic estimate.
    contamination = config.contamination or max(min(y_train.mean(), 0.5), 0.001)

    model = train_model(X_train, config, contamination)
    metrics, anomaly_scores, y_pred = evaluate_model(model, X_test, y_test)
    per_attack = evaluate_per_attack_type(df_test, y_pred)
    metrics["per_attack_type_recall"] = per_attack

    save_artifacts(model, fe, metrics, config)
    return model, fe, metrics


if __name__ == "__main__":
    run_pipeline()