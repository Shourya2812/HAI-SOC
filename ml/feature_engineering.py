"""ml/preprocessing.py

Shared preprocessing pipeline for all machine learning models
used in the HAI-SOC project.
"""

from typing import List, Tuple

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ml.config import ML_DATASET, RANDOM_STATE, TEST_SIZE

TARGET_COLUMN = "label"

DROP_COLUMNS = [
    "timestamp",
    "description",
    "patient_id",
    "session_id",
    "attack_type",
    "attack_id",
    "mitre_tactic",
    "mitre_technique",
    "severity",
    "status",
    "rule_id",
]

def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(ML_DATASET)
    print("=" * 60)
    print("HAI-SOC ML PREPROCESSING")
    print("=" * 60)
    print(f"Dataset Shape : {df.shape}")
    return df

def validate_dataset(df: pd.DataFrame) -> None:
    required = set(DROP_COLUMNS + [TARGET_COLUMN])
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

def prepare_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    validate_dataset(df)
    X = df.drop(columns=DROP_COLUMNS + [TARGET_COLUMN])
    y = df[TARGET_COLUMN]
    return X, y

def get_column_types(X: pd.DataFrame) -> Tuple[List[str], List[str]]:
    categorical_columns = X.select_dtypes(include=["object"]).columns.tolist()
    numerical_columns = X.select_dtypes(include=["number"]).columns.tolist()
    return categorical_columns, numerical_columns

def build_preprocessor(categorical_columns: List[str], numerical_columns: List[str]) -> ColumnTransformer:
    categorical_pipeline = Pipeline(
        steps=[("encoder", OneHotEncoder(handle_unknown="ignore"))]
    )
    numerical_pipeline = Pipeline(
        steps=[("scaler", StandardScaler())]
    )
    return ColumnTransformer(
        transformers=[
            ("categorical", categorical_pipeline, categorical_columns),
            ("numerical", numerical_pipeline, numerical_columns),
        ]
    )

def load_and_preprocess_data():
    df = load_dataset()
    X, y = prepare_features(df)
    categorical_columns, numerical_columns = get_column_types(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    preprocessor = build_preprocessor(
        categorical_columns,
        numerical_columns,
    )

    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

    feature_names = preprocessor.get_feature_names_out()

    print("\n" + "=" * 60)
    print("PREPROCESSING SUMMARY")
    print("=" * 60)
    print(f"Training Samples : {X_train.shape[0]}")
    print(f"Testing Samples  : {X_test.shape[0]}")
    print(f"Categorical      : {len(categorical_columns)}")
    print(f"Numerical        : {len(numerical_columns)}")
    print(f"Encoded Features : {len(feature_names)}")
    print("=" * 60)

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor,
        feature_names,
    )

if __name__ == "__main__":
    load_and_preprocess_data()
