"""
rag/mongo_incident.py

Loads HAI-SOC incidents and their authoritative source logs
from MongoDB.

Relationship:

incidents.log_id
        ↓
logs._id
"""

from pymongo import MongoClient
from bson import ObjectId


MONGO_URL = "mongodb://localhost:27017"
MONGO_DATABASE = "hai_soc"


def get_database():
    """
    Connect to the HAI-SOC MongoDB database.
    """

    client = MongoClient(
        MONGO_URL,
        serverSelectionTimeoutMS=5000,
    )

    # Verify connection
    client.admin.command("ping")

    print("✅ Connected to MongoDB")

    return client[MONGO_DATABASE]


def get_incident_with_source_log(incident_id: str):
    """
    Retrieve an incident and its authoritative source log.

    Returns:

        {
            "incident": {...},
            "source_log": {...}
        }

    or None if the incident does not exist.
    """

    db = get_database()

    incidents = db["incidents"]
    logs = db["logs"]

    # ---------------------------------------------------------
    # 1. Find incident
    # ---------------------------------------------------------

    try:
        incident_object_id = ObjectId(incident_id)
    except Exception:
        raise ValueError(
            f"Invalid MongoDB incident ID: {incident_id}"
        )

    incident = incidents.find_one(
        {
            "_id": incident_object_id
        }
    )

    if incident is None:
        return None

    # ---------------------------------------------------------
    # 2. Extract log_id
    # ---------------------------------------------------------

    log_id = incident.get("log_id")

    if not log_id:
        raise ValueError(
            f"Incident {incident_id} does not contain log_id"
        )

    # ---------------------------------------------------------
    # 3. Find authoritative source log
    # ---------------------------------------------------------
    #
    # IMPORTANT:
    #
    # incidents.log_id is stored as a string.
    #
    # logs._id is stored as ObjectId.
    #
    # Therefore convert log_id → ObjectId.
    #

    try:
        log_object_id = ObjectId(log_id)
    except Exception:
        raise ValueError(
            f"Invalid log_id '{log_id}' in incident "
            f"{incident_id}"
        )

    source_log = logs.find_one(
        {
            "_id": log_object_id
        }
    )

    if source_log is None:
        raise ValueError(
            f"Authoritative source log not found for "
            f"incident {incident_id}. "
            f"log_id={log_id}"
        )

    # ---------------------------------------------------------
    # 4. Return both
    # ---------------------------------------------------------

    return {
        "incident": incident,
        "source_log": source_log,
    }


if __name__ == "__main__":

    # ---------------------------------------------------------
    # Test with the incident currently present in MongoDB.
    # ---------------------------------------------------------

    incident_id = "6a80c6b1c091aba98edbbc23"

    result = get_incident_with_source_log(
        incident_id
    )

    if result is None:

        print("❌ Incident not found")

    else:

        incident = result["incident"]
        source_log = result["source_log"]

        print("\n" + "=" * 70)
        print("INCIDENT")
        print("=" * 70)

        print("ID:", incident["_id"])
        print("Title:", incident.get("title"))
        print("Description:", incident.get("description"))
        print("Detector:", incident.get("detector"))
        print("Anomaly Score:", incident.get("anomaly_score"))
        print("Risk Level:", incident.get("risk_level"))
        print("Log ID:", incident.get("log_id"))

        print("\n" + "=" * 70)
        print("AUTHORITATIVE SOURCE LOG")
        print("=" * 70)

        print("ID:", source_log["_id"])
        print("Timestamp:", source_log.get("timestamp"))
        print("Source:", source_log.get("source"))
        print("Destination:", source_log.get("destination"))
        print("User ID:", source_log.get("user_id"))
        print("Role:", source_log.get("role"))
        print("Device:", source_log.get("device"))
        print("Department:", source_log.get("department"))
        print("Action:", source_log.get("action"))
        print("Severity:", source_log.get("severity"))
        print("Protocol:", source_log.get("protocol"))
        print("Port:", source_log.get("port"))
        print("Outcome:", source_log.get("outcome"))
        print("Extra:", source_log.get("extra"))