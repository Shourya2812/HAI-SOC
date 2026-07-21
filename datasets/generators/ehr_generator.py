import json
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from behavior import generate_workflow

from utils import (
    generate_ip,
    generate_patient_id,
    generate_base_timestamp,
)

from constants import (
    USERS,
    ASSETS,
    EVENT_SEVERITY,
    EVENT_DESCRIPTIONS,
)

def generate_ehr_session():
    """
    Generate one realistic EHR user session.
    """

    user = random.choice(USERS)
    workflow = generate_workflow(user["role"])

    asset = random.choice(ASSETS)

    session_id = str(uuid.uuid4())

    base_time = generate_base_timestamp(user["role"])

    logs = []

    for i, event in enumerate(workflow):

        log = {
            "timestamp": (
                base_time + timedelta(minutes=i * random.randint(1, 3))
            ).isoformat(),

            "source": "EHR",

            "event_type": event,

            "user": user["username"],

            "user_role": user["role"],

            "department": user["department"],

            "asset": asset,

            "severity": EVENT_SEVERITY[event],

            "status": "SUCCESS",

            "source_ip": generate_ip(),

            "destination_ip": "10.0.0.10",

            "description": EVENT_DESCRIPTIONS[event],

            "extra": {
                "patient_id": generate_patient_id(),
                "session_id": session_id,
            },
        }

        logs.append(log)

    return logs


def save_logs(logs, filename="ehr_logs.json"):
    """
    Save generated logs to datasets/raw/
    """

    output_dir = Path(__file__).parent.parent / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / filename

    with open(output_file, "w") as f:
        json.dump(logs, f, indent=4)

    print(f"Saved {len(logs)} logs to {output_file}")


if __name__ == "__main__":

    logs = []

    NUM_SESSIONS = 100

    for _ in range(NUM_SESSIONS):
        session_logs = generate_ehr_session()
        logs.extend(session_logs)

    save_logs(logs)