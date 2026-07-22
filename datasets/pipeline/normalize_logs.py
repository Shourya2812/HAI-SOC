"""
Normalize merged healthcare security logs into a canonical schema.

Input:
    datasets/processed/unified_logs.json

Output:
    datasets/processed/normalized_logs.json
"""

from pathlib import Path
import json


# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "processed"

INPUT_FILE = PROCESSED_DIR / "unified_logs.json"
OUTPUT_FILE = PROCESSED_DIR / "normalized_logs.json"


# ==========================================================
# Canonical Schema
# ==========================================================

CANONICAL_FIELDS = [
    "timestamp",
    "source",
    "event_type",
    "severity",
    "status",
    "user",
    "role",
    "department",
    "asset",
    "source_ip",
    "destination_ip",
    "description",
]


# ==========================================================
# Helper Functions
# ==========================================================

def load_logs():
    """
    Load merged logs.
    """

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_log(log: dict) -> dict:
    """
    Convert one log event into the canonical schema.
    """

    normalized = {}

    normalized["timestamp"] = log.get("timestamp")
    normalized["source"] = log.get("source")
    normalized["event_type"] = log.get("event_type")
    normalized["severity"] = log.get("severity")
    normalized["status"] = log.get("status")
    normalized["user"] = log.get("user")

    # Normalize role
    normalized["role"] = (
        log.get("role")
        or log.get("user_role")
    )

    normalized["department"] = log.get("department")
    normalized["asset"] = log.get("asset")
    normalized["source_ip"] = log.get("source_ip")
    normalized["destination_ip"] = log.get("destination_ip")
    normalized["description"] = log.get("description", "")

    # Collect all remaining fields
    extra = {}

    for key, value in log.items():

        if key in CANONICAL_FIELDS:
            continue

        # Skip fields that were normalized
        if key == "user_role":
            continue

        # Flatten nested extra
        if key == "extra" and isinstance(value, dict):
            extra.update(value)
        else:
            extra[key] = value

    normalized["extra"] = extra

    return normalized

def normalize_logs(logs: list) -> list:
    """
    Normalize every log in the dataset.
    """

    return [normalize_log(log) for log in logs]


def save_logs(logs: list):
    """
    Save normalized logs.
    """

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)

    print(f"\nNormalized dataset saved to:\n{OUTPUT_FILE}")


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("Healthcare Log Normalizer")
    print("=" * 60)

    logs = load_logs()

    print(f"\nLoaded {len(logs)} merged logs")

    normalized_logs = normalize_logs(logs)

    save_logs(normalized_logs)

    print(f"Normalized {len(normalized_logs)} events")

    print("\nNormalization completed successfully.")


if __name__ == "__main__":
    main()