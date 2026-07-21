import random
from datetime import datetime, timedelta
from behavior import WORKING_HOURS


def generate_ip():
    """Generate a random private IPv4 address."""
    return (
        f"10.{random.randint(0,255)}."
        f"{random.randint(0,255)}."
        f"{random.randint(1,254)}"
    )


def generate_patient_id():
    """Generate a random patient ID."""
    return f"P{random.randint(1000,9999)}"


def generate_base_timestamp(role):
    start_hour, end_hour = WORKING_HOURS[role]

    days_ago = random.randint(0, 6)

    hour = random.randint(start_hour, end_hour)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    base_date = datetime.now() - timedelta(days=days_ago)

    return base_date.replace(
        hour=hour,
        minute=minute,
        second=second,
        microsecond=0,
    )