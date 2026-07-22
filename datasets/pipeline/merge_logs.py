"""
Merge logs from multiple healthcare data sources into a single
chronologically ordered event stream.

Input:
    datasets/raw/
        - ehr_logs.json
        - vpn_logs.json
        - firewall_logs.json

Output:
    datasets/processed/unified_logs.json
"""

from pathlib import Path
import json


# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"

PROCESSED_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = PROCESSED_DIR / "unified_logs.json"

LOG_FILES = [
    RAW_DIR / "ehr_logs.json",
    RAW_DIR / "vpn_logs.json",
    RAW_DIR / "firewall_logs.json",
]


# ==========================================================
# Helper Functions
# ==========================================================

def load_logs(file_path: Path) -> list:
    """
    Load logs from a JSON file.

    Returns:
        list of log events
    """

    if not file_path.exists():
        print(f"[WARNING] Missing file: {file_path.name}")
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def merge_logs() -> list:
    """
    Merge all available log files.
    """

    merged_logs = []

    for log_file in LOG_FILES:
        logs = load_logs(log_file)

        print(f"Loaded {len(logs)} logs from {log_file.name}")

        merged_logs.extend(logs)

    return merged_logs


def sort_logs(logs: list) -> list:
    """
    Sort logs by timestamp.
    """

    return sorted(
        logs,
        key=lambda log: log["timestamp"]
    )


def save_logs(logs: list):
    """
    Save merged logs.
    """

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)

    print(f"\nMerged dataset saved to:\n{OUTPUT_FILE}")


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("Healthcare Log Merger")
    print("=" * 60)

    logs = merge_logs()

    print(f"\nTotal logs before sorting : {len(logs)}")

    logs = sort_logs(logs)

    save_logs(logs)

    print(f"Total logs after sorting  : {len(logs)}")

    print("\nMerge completed successfully.")


if __name__ == "__main__":
    main()