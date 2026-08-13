"""
HAI-SOC Synthetic Healthcare Security Log Generator

Usage:

    python backend/scripts/generate_security_logs.py

    python backend/scripts/generate_security_logs.py --reset

--reset:
    Clears ONLY the MongoDB `logs` collection before inserting
    the synthetic dataset.

It does NOT modify:
    - anomaly_scores
    - incidents
    - users
"""

import argparse
import random
from datetime import datetime, timedelta, timezone

from backend.app.database.collections import logs_collection
from backend.app.models.enums import Outcome, Severity, UserRole


# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42

TOTAL_LOGS = 2000

NORMAL_COUNT = 1700
SUSPICIOUS_COUNT = 200
ANOMALOUS_COUNT = 100

random.seed(SEED)


# ============================================================
# HEALTHCARE SOURCES
# ============================================================

SOURCES = [
    "EHR",
    "PACS",
    "Firewall",
    "VPN",
    "ActiveDirectory",
    "Database",
    "IoMT",
    "API_Gateway",
]


DESTINATIONS = {
    "EHR": [
        "EHR_Server",
        "EHR_DB",
    ],
    "PACS": [
        "PACS_Server",
        "Imaging_DB",
    ],
    "Firewall": [
        "EHR_Server",
        "PACS_Server",
        "Internet",
    ],
    "VPN": [
        "VPN_Gateway",
        "EHR_Server",
    ],
    "ActiveDirectory": [
        "AD_Server",
    ],
    "Database": [
        "EHR_DB",
        "Patient_DB",
    ],
    "IoMT": [
        "IoMT_Gateway",
        "Monitoring_Server",
    ],
    "API_Gateway": [
        "FHIR_API",
        "EHR_Server",
    ],
}


# ============================================================
# HEALTHCARE DEPARTMENTS
# ============================================================

DEPARTMENTS = [
    "CARDIOLOGY",
    "RADIOLOGY",
    "EMERGENCY",
    "PHARMACY",
    "ONCOLOGY",
    "NEUROLOGY",
    "ADMINISTRATION",
    "IT",
]


# ============================================================
# USERS
# ============================================================

USERS = [
    ("USR001", UserRole.DOCTOR, "CARDIOLOGY"),
    ("USR002", UserRole.DOCTOR, "RADIOLOGY"),
    ("USR003", UserRole.NURSE, "EMERGENCY"),
    ("USR004", UserRole.NURSE, "ONCOLOGY"),
    ("USR005", UserRole.DOCTOR, "NEUROLOGY"),
    ("USR006", UserRole.ADMIN, "ADMINISTRATION"),
    ("USR007", UserRole.SOC_ANALYST, "IT"),
    ("USR008", UserRole.SYSTEM, "IT"),
    ("USR009", UserRole.DOCTOR, "PHARMACY"),
    ("USR010", UserRole.NURSE, "CARDIOLOGY"),
]


# ============================================================
# ACTIONS
# ============================================================

NORMAL_ACTIONS = [
    "LOGIN",
    "LOGOUT",
    "READ_PATIENT_RECORD",
    "UPDATE_PATIENT_RECORD",
    "QUERY_DATABASE",
    "FILE_ACCESS",
    "IMAGE_ACCESS",
    "NETWORK_CONNECTION",
    "DEVICE_TELEMETRY",
    "API_REQUEST",
]


SUSPICIOUS_ACTIONS = [
    "EXPORT_PHI",
    "QUERY_DATABASE",
    "FILE_ACCESS",
    "LOGIN",
    "NETWORK_CONNECTION",
    "API_REQUEST",
]


ANOMALOUS_ACTIONS = [
    "EXPORT_PHI",
    "FIRMWARE_UPDATE",
    "LOGIN",
    "QUERY_DATABASE",
    "NETWORK_CONNECTION",
]


# ============================================================
# TIMESTAMP GENERATION
# ============================================================

def make_timestamp(days_back: int = 7) -> datetime:
    """
    Generate a timestamp within the previous few days.

    Normal activity is biased toward normal working hours,
    while suspicious/anomalous events will later be explicitly
    shifted toward unusual hours.
    """

    now = datetime.now(timezone.utc)

    day_offset = random.randint(0, days_back)

    base = now - timedelta(days=day_offset)

    hour = random.choices(
        population=list(range(24)),
        weights=[
            1,   # 00
            1,   # 01
            1,   # 02
            1,   # 03
            1,   # 04
            2,   # 05
            4,   # 06
            6,   # 07
            8,   # 08
            10,  # 09
            10,  # 10
            10,  # 11
            10,  # 12
            10,  # 13
            10,  # 14
            10,  # 15
            10,  # 16
            8,   # 17
            6,   # 18
            5,   # 19
            3,   # 20
            2,   # 21
            1,   # 22
            1,   # 23
        ],
    )[0]

    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    return base.replace(
        hour=hour,
        minute=minute,
        second=second,
        microsecond=random.randint(0, 999999),
    )


# ============================================================
# USER SELECTION
# ============================================================

def choose_user():
    return random.choice(USERS)


# ============================================================
# NORMAL LOG
# ============================================================

def generate_normal_log():

    user_id, role, department = choose_user()

    source = random.choice(SOURCES)

    destination = random.choice(
        DESTINATIONS[source]
    )

    action = random.choice(
        NORMAL_ACTIONS
    )

    timestamp = make_timestamp()

    severity = random.choices(
        [
            Severity.LOW,
            Severity.MEDIUM,
        ],
        weights=[
            90,
            10,
        ],
    )[0]

    outcome = random.choices(
        [
            Outcome.SUCCESS,
            Outcome.FAILURE,
        ],
        weights=[
            97,
            3,
        ],
    )[0]

    protocol = random.choice(
        [
            "HTTPS",
            "TCP",
            "UDP",
        ]
    )

    if protocol == "HTTPS":
        port = 443

    elif protocol == "TCP":
        port = random.choice(
            [
                80,
                443,
                1433,
                5432,
            ]
        )

    else:
        port = random.choice(
            [
                53,
                123,
            ]
        )

    extra = {
        "bytes_sent": random.randint(
            512,
            50000,
        ),
        "session_duration": random.randint(
            30,
            3600,
        ),
    }

    return {
        "timestamp": timestamp,

        "source": source,

        "destination": destination,

        "user_id": user_id,

        "role": role.value,

        "device": (
            f"WS-{random.randint(1, 100):03d}"
        ),

        "department": department,

        "action": action,

        "severity": severity.value,

        "protocol": protocol,

        "port": port,

        "message": (
            f"Normal "
            f"{action.lower().replace('_', ' ')} "
            f"activity"
        ),

        "outcome": outcome.value,

        "extra": extra,
    }


# ============================================================
# SUSPICIOUS LOG
# ============================================================

def generate_suspicious_log():

    user_id, role, department = choose_user()

    source = random.choice(
        [
            "EHR",
            "PACS",
            "VPN",
            "Database",
            "API_Gateway",
        ]
    )

    destination = random.choice(
        DESTINATIONS[source]
    )

    action = random.choice(
        SUSPICIOUS_ACTIONS
    )

    timestamp = make_timestamp()

    # Force suspicious activity toward unusual hours.
    timestamp = timestamp.replace(
        hour=random.choice(
            [
                0,
                1,
                2,
                3,
                4,
                5,
                22,
                23,
            ]
        )
    )

    severity = random.choices(
        [
            Severity.MEDIUM,
            Severity.HIGH,
        ],
        weights=[
            65,
            35,
        ],
    )[0]

    outcome = random.choices(
        [
            Outcome.SUCCESS,
            Outcome.FAILURE,
        ],
        weights=[
            75,
            25,
        ],
    )[0]

    extra = {
        "bytes_sent": random.randint(
            50000,
            5000000,
        ),

        "failed_attempts": random.randint(
            0,
            5,
        ),

        "unusual_hour": True,
    }

    if action == "EXPORT_PHI":

        extra["records_accessed"] = random.randint(
            50,
            300,
        )

    return {
        "timestamp": timestamp,

        "source": source,

        "destination": destination,

        "user_id": user_id,

        "role": role.value,

        "device": (
            f"WS-{random.randint(1, 100):03d}"
        ),

        "department": department,

        "action": action,

        "severity": severity.value,

        "protocol": random.choice(
            [
                "HTTPS",
                "TCP",
            ]
        ),

        "port": random.choice(
            [
                443,
                80,
                5432,
            ]
        ),

        "message": (
            f"Suspicious "
            f"{action.lower().replace('_', ' ')} "
            f"activity"
        ),

        "outcome": outcome.value,

        "extra": extra,
    }


# ============================================================
# ANOMALOUS LOG
# ============================================================

def generate_anomalous_log():

    user_id, role, department = choose_user()

    source = random.choice(
        [
            "EHR",
            "Database",
            "Firewall",
            "IoMT",
            "ActiveDirectory",
        ]
    )

    destination = random.choice(
        DESTINATIONS[source]
    )

    action = random.choice(
        ANOMALOUS_ACTIONS
    )

    timestamp = make_timestamp()

    # Strongly unusual access time.
    timestamp = timestamp.replace(
        hour=random.choice(
            [
                0,
                1,
                2,
                3,
                4,
            ]
        )
    )

    severity = random.choices(
        [
            Severity.HIGH,
            Severity.CRITICAL,
        ],
        weights=[
            35,
            65,
        ],
    )[0]

    outcome = random.choices(
        [
            Outcome.SUCCESS,
            Outcome.FAILURE,
        ],
        weights=[
            80,
            20,
        ],
    )[0]

    extra = {
        "bytes_sent": random.randint(
            10000000,
            250000000,
        ),

        "failed_attempts": random.randint(
            5,
            20,
        ),

        "unusual_hour": True,

        "records_accessed": random.randint(
            100,
            1000,
        ),
    }

    if action == "FIRMWARE_UPDATE":

        extra.update(
            {
                "firmware_version": (
                    f"v"
                    f"{random.randint(1, 9)}."
                    f"{random.randint(0, 9)}"
                ),

                "unauthorized": True,
            }
        )

    if action == "EXPORT_PHI":

        extra["mass_export"] = True

    return {
        "timestamp": timestamp,

        "source": source,

        "destination": destination,

        "user_id": user_id,

        "role": role.value,

        "device": (
            f"WS-{random.randint(1, 100):03d}"
        ),

        "department": department,

        "action": action,

        "severity": severity.value,

        "protocol": random.choice(
            [
                "HTTPS",
                "TCP",
            ]
        ),

        "port": random.choice(
            [
                443,
                5432,
                1433,
            ]
        ),

        "message": (
            f"Critical "
            f"{action.lower().replace('_', ' ')} "
            f"detected"
        ),

        "outcome": outcome.value,

        "extra": extra,
    }


# ============================================================
# DATASET GENERATION
# ============================================================

def generate_dataset():

    logs = []

    # -------------------------
    # Normal
    # -------------------------

    for _ in range(NORMAL_COUNT):

        logs.append(
            generate_normal_log()
        )

    # -------------------------
    # Suspicious
    # -------------------------

    for _ in range(SUSPICIOUS_COUNT):

        logs.append(
            generate_suspicious_log()
        )

    # -------------------------
    # Anomalous
    # -------------------------

    for _ in range(ANOMALOUS_COUNT):

        logs.append(
            generate_anomalous_log()
        )

    # Shuffle so the dataset isn't ordered
    # NORMAL → SUSPICIOUS → ANOMALOUS.

    random.shuffle(logs)

    return logs


# ============================================================
# VALIDATION
# ============================================================

def validate_dataset(logs):

    assert len(logs) == TOTAL_LOGS

    required_fields = {
        "timestamp",
        "source",
        "destination",
        "user_id",
        "role",
        "device",
        "department",
        "action",
        "severity",
        "protocol",
        "port",
        "message",
        "outcome",
        "extra",
    }

    for index, log in enumerate(logs):

        missing = required_fields - set(
            log.keys()
        )

        if missing:

            raise ValueError(
                f"Log {index} missing fields: "
                f"{missing}"
            )

        if log["severity"] not in {
            severity.value
            for severity in Severity
        }:

            raise ValueError(
                f"Invalid severity in log {index}: "
                f"{log['severity']}"
            )

        if log["outcome"] not in {
            outcome.value
            for outcome in Outcome
        }:

            raise ValueError(
                f"Invalid outcome in log {index}: "
                f"{log['outcome']}"
            )

        if log["role"] not in {
            role.value
            for role in UserRole
        }:

            raise ValueError(
                f"Invalid role in log {index}: "
                f"{log['role']}"
            )


# ============================================================
# DATABASE INSERTION
# ============================================================

def insert_dataset(logs):

    result = logs_collection.insert_many(
        logs
    )

    return result.inserted_ids


# ============================================================
# STATISTICS
# ============================================================

def print_statistics():

    total = logs_collection.count_documents({})

    print()
    print("=" * 55)
    print("HAI-SOC SYNTHETIC DATASET")
    print("=" * 55)

    print(
        f"Total logs: {total}"
    )

    print()
    print("Severity Distribution")
    print("-" * 30)

    for severity in Severity:

        count = logs_collection.count_documents(
            {
                "severity": severity.value
            }
        )

        print(
            f"{severity.value:<12} : {count}"
        )

    print()
    print("Source Distribution")
    print("-" * 30)

    for source in SOURCES:

        count = logs_collection.count_documents(
            {
                "source": source
            }
        )

        print(
            f"{source:<18} : {count}"
        )

    print()
    print("Outcome Distribution")
    print("-" * 30)

    for outcome in Outcome:

        count = logs_collection.count_documents(
            {
                "outcome": outcome.value
            }
        )

        print(
            f"{outcome.value:<12} : {count}"
        )

    print()
    print("Department Distribution")
    print("-" * 30)

    for department in DEPARTMENTS:

        count = logs_collection.count_documents(
            {
                "department": department
            }
        )

        print(
            f"{department:<18} : {count}"
        )

    print()
    print("=" * 55)


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Generate synthetic HAI-SOC "
            "healthcare security logs."
        )
    )

    parser.add_argument(
        "--reset",
        action="store_true",
        help=(
            "Delete all existing logs before "
            "inserting the generated dataset."
        ),
    )

    args = parser.parse_args()

    # -------------------------
    # Reset logs if requested
    # -------------------------

    if args.reset:

        result = logs_collection.delete_many({})

        print(
            f"Deleted "
            f"{result.deleted_count} "
            f"existing logs."
        )

    # -------------------------
    # Generate
    # -------------------------

    print(
        f"Generating {TOTAL_LOGS} "
        "synthetic healthcare security logs..."
    )

    logs = generate_dataset()

    # -------------------------
    # Validate
    # -------------------------

    print(
        "Validating generated dataset..."
    )

    validate_dataset(logs)

    print(
        "Dataset validation passed."
    )

    # -------------------------
    # Insert
    # -------------------------

    print(
        "Inserting logs into MongoDB..."
    )

    inserted_ids = insert_dataset(
        logs
    )

    print(
        f"Inserted {len(inserted_ids)} logs."
    )

    # -------------------------
    # Statistics
    # -------------------------

    print_statistics()


if __name__ == "__main__":

    main()