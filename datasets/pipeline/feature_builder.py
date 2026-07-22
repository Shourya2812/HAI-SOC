"""
Feature Engineering Pipeline

Input:
    datasets/processed/validated_logs.json

Output:
    datasets/processed/features.csv
"""

from pathlib import Path
from datetime import datetime
import json
import pandas as pd

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "processed"

INPUT_FILE = PROCESSED_DIR / "validated_logs.json"
OUTPUT_FILE = PROCESSED_DIR / "features.csv"

# ==========================================================
# Encoding Maps
# ==========================================================

SEVERITY_SCORE = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4
}

STATUS_SCORE = {
    "SUCCESS": 0,
    "FAILED": 1,
    "BLOCKED": 1
}

BUSINESS_START = 8
BUSINESS_END = 18

# ==========================================================
# Load Data
# ==========================================================

def load_logs():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ==========================================================
# Feature Extraction
# ==========================================================

def extract_features(log):

    row = {}

    # ------------------------------------------------------
    # Timestamp Features
    # ------------------------------------------------------

    ts = datetime.fromisoformat(log["timestamp"])

    row["timestamp"] = log["timestamp"]
    row["hour"] = ts.hour
    row["day_of_week"] = ts.weekday()
    row["month"] = ts.month

    row["is_weekend"] = int(ts.weekday() >= 5)

    row["is_business_hours"] = int(
        BUSINESS_START <= ts.hour < BUSINESS_END
    )

    # ------------------------------------------------------
    # Basic Fields
    # ------------------------------------------------------

    row["source"] = log.get("source")

    row["event_type"] = log.get("event_type")

    row["user"] = log.get("user")

    row["role"] = log.get("role")

    row["department"] = log.get("department")

    row["asset"] = log.get("asset")

    row["source_ip"] = log.get("source_ip")

    row["destination_ip"] = log.get("destination_ip")

    # ------------------------------------------------------
    # Encoded Features
    # ------------------------------------------------------

    severity = log.get("severity")

    row["severity"] = severity

    row["severity_score"] = SEVERITY_SCORE.get(severity, 0)

    status = log.get("status")

    row["status"] = status

    row["status_score"] = STATUS_SCORE.get(status, 0)

    # ------------------------------------------------------
    # Description
    # ------------------------------------------------------

    row["description"] = log.get("description")

    # ------------------------------------------------------
    # Flatten Extra Dictionary
    # ------------------------------------------------------

    extra = log.get("extra", {})

    if isinstance(extra, dict):

        for key, value in extra.items():
            row[key] = value

    # ------------------------------------------------------
    # Label
    # ------------------------------------------------------

    row["label"] = 0

    return row


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("Healthcare Feature Builder")
    print("=" * 60)

    logs = load_logs()

    print(f"\nLoaded {len(logs)} validated logs")

    feature_rows = []

    for log in logs:
        feature_rows.append(extract_features(log))

    df = pd.DataFrame(feature_rows)

    # Fill missing values

    # Fill categorical columns
    object_cols = df.select_dtypes(include="object").columns
    df[object_cols] = df[object_cols].fillna("N/A")

    # Fill numeric columns
    numeric_cols = df.select_dtypes(include=["number"]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # Save

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nFeatures Generated : {len(df)}")

    print(f"Columns            : {len(df.columns)}")

    print(f"\nSaved to\n{OUTPUT_FILE}")

    print("\nFeature engineering completed successfully.")


if __name__ == "__main__":
    main()