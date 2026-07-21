import json
import random
from pathlib import Path
from datetime import timedelta

from utils import (
    generate_ip,
    generate_base_timestamp,
)

from constants import (
    EVENT_SEVERITY,
    EVENT_DESCRIPTIONS,
)

FIREWALL_EVENTS = [
    "ALLOW",
    "DENY",
    "BLOCKED_PORT_SCAN",
    "BLOCKED_IP",
]

PROTOCOLS = [
    "TCP",
    "UDP",
]

COMMON_PORTS = [
    22,
    53,
    80,
    443,
    3306,
    5432,
    8080,
]

RULE_IDS = [
    "FW-101",
    "FW-102",
    "FW-201",
    "FW-301",
]


def generate_firewall_log():
    """
    Generate one realistic firewall log.
    """

    event = random.choice(FIREWALL_EVENTS)

    protocol = random.choice(PROTOCOLS)

    destination_port = random.choice(COMMON_PORTS)

    rule_id = random.choice(RULE_IDS)

    bytes_sent = random.randint(500, 50000)

    log = {

        "timestamp": generate_base_timestamp("ADMIN").isoformat(),

        "source": "FIREWALL",

        "event_type": event,

        "source_ip": generate_ip(),

        "destination_ip": generate_ip(),

        "destination_port": destination_port,

        "protocol": protocol,

        "severity": EVENT_SEVERITY[event],

        "status": "SUCCESS" if event == "ALLOW" else "BLOCKED",

        "description": EVENT_DESCRIPTIONS[event],

        "extra": {
            "rule_id": rule_id,
            "bytes_sent": bytes_sent,
        },
    }

    return log


def save_logs(logs, filename="firewall_logs.json"):
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

    NUM_LOGS = 1000

    for _ in range(NUM_LOGS):
        logs.append(generate_firewall_log())

    save_logs(logs)