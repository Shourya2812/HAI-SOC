"""
Validate normalized healthcare security logs.

Input:
    datasets/processed/normalized_logs.json

Outputs:
    datasets/processed/validated_logs.json
    datasets/processed/invalid_logs.json
    datasets/processed/validation_report.json
"""

from pathlib import Path
import json
from datetime import datetime
import ipaddress
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config.validation_rules import (
    REQUIRED_FIELDS,
    VALID_STATUS,
    VALID_SEVERITIES,
    VALID_SOURCES
)

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "processed"

INPUT_FILE = PROCESSED_DIR / "normalized_logs.json"

VALID_OUTPUT = PROCESSED_DIR / "validated_logs.json"
INVALID_OUTPUT = PROCESSED_DIR / "invalid_logs.json"
REPORT_OUTPUT = PROCESSED_DIR / "validation_report.json"

# ==========================================================
# Helper Functions
# ==========================================================

def load_logs():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def is_valid_ip(ip):

    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_valid_timestamp(timestamp):

    try:
        datetime.fromisoformat(timestamp)
        return True
    except ValueError:
        return False


# ==========================================================
# Validation
# ==========================================================

def validate_log(log):

    errors = []

    source = log.get("source")

    # ----------------------------
    # Source Validation
    # ----------------------------

    if source not in VALID_SOURCES:
        errors.append("Invalid source")
        return errors

    required_fields = REQUIRED_FIELDS[source]

    # ----------------------------
    # Required Fields
    # ----------------------------

    for field in required_fields:

        if field not in log:
            errors.append(f"Missing field: {field}")
            continue

        value = log[field]

        if value is None:
            errors.append(f"Null value: {field}")

        elif isinstance(value, str) and value.strip() == "":
            errors.append(f"Empty value: {field}")

    # ----------------------------
    # Timestamp
    # ----------------------------

    if "timestamp" in log:

        if not is_valid_timestamp(log["timestamp"]):
            errors.append("Invalid timestamp")

    # ----------------------------
    # Severity
    # ----------------------------

    if log.get("severity") not in VALID_SEVERITIES:
        errors.append("Invalid severity")

    # ----------------------------
    # Status
    # ----------------------------

    if log.get("status") not in VALID_STATUS[source]:
        errors.append("Invalid status")

    # ----------------------------
    # IP Addresses
    # ----------------------------

    if not is_valid_ip(log.get("source_ip", "")):
        errors.append("Invalid source IP")

    if not is_valid_ip(log.get("destination_ip", "")):
        errors.append("Invalid destination IP")

    # ----------------------------
    # Extra
    # ----------------------------

    if not isinstance(log.get("extra"), dict):
        errors.append("Extra must be a dictionary")

    return errors


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("Healthcare Log Validator")
    print("=" * 60)

    logs = load_logs()

    valid_logs = []
    invalid_logs = []

    report = {
        "total_logs": len(logs),
        "valid_logs": 0,
        "invalid_logs": 0,
        "error_summary": {}
    }

    for log in logs:

        errors = validate_log(log)

        if errors:

            invalid_logs.append({
                "log": log,
                "errors": errors
            })

            for err in errors:
                report["error_summary"][err] = (
                    report["error_summary"].get(err, 0) + 1
                )

        else:
            valid_logs.append(log)

    report["valid_logs"] = len(valid_logs)
    report["invalid_logs"] = len(invalid_logs)

    save_json(VALID_OUTPUT, valid_logs)
    save_json(INVALID_OUTPUT, invalid_logs)
    save_json(REPORT_OUTPUT, report)

    print(f"\nTotal Logs      : {report['total_logs']}")
    print(f"Valid Logs      : {report['valid_logs']}")
    print(f"Invalid Logs    : {report['invalid_logs']}")

    print("\nValidation Report")

    if report["error_summary"]:

        for error, count in report["error_summary"].items():
            print(f"{error:<35}{count}")

    else:
        print("No validation errors found.")

    print("\nFiles Generated")

    print(f"✓ {VALID_OUTPUT}")
    print(f"✓ {INVALID_OUTPUT}")
    print(f"✓ {REPORT_OUTPUT}")

    print("\nValidation completed successfully.")


if __name__ == "__main__":
    main()