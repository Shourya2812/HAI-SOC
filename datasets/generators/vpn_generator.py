import json
import random
import uuid
from pathlib import Path
from datetime import timedelta

from utils import (
    generate_ip,
    generate_base_timestamp,
)

from constants import (
    USERS,
    EVENT_SEVERITY,
    EVENT_DESCRIPTIONS,
)

VPN_EVENTS = [
    "VPN_LOGIN",
    "VPN_CONNECTED",
    "VPN_LOGOUT",
]


def generate_vpn_session():
    """
    Generate one realistic VPN session.
    """

    user = random.choice(USERS)

    session_id = str(uuid.uuid4())

    base_time = generate_base_timestamp(user["role"])

    source_ip = generate_ip()

    logs = []

    for i, event in enumerate(VPN_EVENTS):

        log = {
            "timestamp": (
                base_time + timedelta(minutes=i)
            ).isoformat(),

            "source": "VPN",

            "event_type": event,

            "user": user["username"],

            "user_role": user["role"],

            "department": user["department"],

            "source_ip": source_ip,

            "destination_ip": "10.0.0.5",

            "severity": EVENT_SEVERITY[event],

            "status": "SUCCESS",

            "description": EVENT_DESCRIPTIONS[event],

            "extra": {
                "session_id": session_id,
                "vpn_gateway": "VPN-GW-01",
            },
        }

        logs.append(log)

    return logs


def save_logs(logs, filename="vpn_logs.json"):

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
        logs.extend(generate_vpn_session())

    save_logs(logs)