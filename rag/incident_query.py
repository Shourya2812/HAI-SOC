"""
rag/incident_query.py

Builds semantic retrieval queries from HAI-SOC incidents
and retrieves the authoritative source log from MongoDB.
"""

from typing import Optional

from bson import ObjectId

from backend.app.database.collections import logs_collection
from rag.retriever import retrieve_knowledge, print_results


def get_source_log(incident: dict) -> Optional[dict]:
    """
    Retrieve the original security log associated with an incident.

    The incident's log_id is the authoritative link between the
    incident and the original security event.
    """

    log_id = incident.get("log_id")

    if not log_id:
        return None

    # MongoDB logs use ObjectId as their _id.
    try:
        document = logs_collection.find_one(
            {
                "_id": ObjectId(log_id)
            }
        )
    except Exception:
        return None

    if document is None:
        return None

    # Convert MongoDB ObjectId to a JSON-friendly string.
    document["id"] = str(document["_id"])
    document.pop("_id", None)

    return document


def build_incident_query(incident: dict, source_log: Optional[dict] = None) -> str:
    """
    Convert an HAI-SOC incident and its source log into a
    semantic retrieval query.

    The incident and source log are treated as factual context
    for retrieval. Retrieved knowledge is used only to identify
    relevant HIPAA, NIST, MITRE, and runbook information.
    """

    title = incident.get("title", "")
    description = incident.get("description", "")
    detector = incident.get("detector", "")
    anomaly_score = incident.get("anomaly_score", "")
    risk_level = incident.get("risk_level", "")
    log_id = incident.get("log_id", "")

    if source_log is None:
        source_log = get_source_log(incident)

    log_context = ""

    if source_log:

        log_context = f"""
Source Log:

Source: {source_log.get("source", "")}
Destination: {source_log.get("destination", "")}
User ID: {source_log.get("user_id", "")}
Role: {source_log.get("role", "")}
Device: {source_log.get("device", "")}
Department: {source_log.get("department", "")}
Action: {source_log.get("action", "")}
Severity: {source_log.get("severity", "")}
Protocol: {source_log.get("protocol", "")}
Port: {source_log.get("port", "")}
Outcome: {source_log.get("outcome", "")}

Additional telemetry:

{source_log.get("extra", {})}
""".strip()

    else:

        log_context = (
            "Source Log: Not available in current telemetry."
        )

    return f"""
Healthcare security incident.

Incident:

Title: {title}

Description: {description}

Detector: {detector}

Anomaly score: {anomaly_score}

Risk level: {risk_level}

Source log ID: {log_id}

{log_context}

Identify relevant:

- HIPAA compliance requirements
- NIST security controls
- MITRE ATT&CK techniques
- Healthcare SOC incident response runbooks

Use the incident and source log as factual telemetry.

Do not assume that a security action proves compromise,
unauthorized access, or data exfiltration.

Focus on evidence, investigation steps, compliance implications,
threat techniques, and recommended response actions.
""".strip()


if __name__ == "__main__":

    # Test incident representing an actual HAI-SOC event.
    incident = {
        "title": "Security Anomaly: EXPORT_PHI",
        "description": (
            "Anomalous activity detected in PACS "
            "by xgboost_v1."
        ),
        "detector": "xgboost_v1",
        "anomaly_score": 0.999,
        "risk_level": "CRITICAL",
        "log_id": "6a7e127a168d270fdd2ed85f",
    }

    source_log = get_source_log(incident)

    print("\nSource Log:\n")

    if source_log:
        print(source_log)
    else:
        print("Source log not found.")

    query = build_incident_query(incident)

    print("\nGenerated Incident Query:\n")
    print(query)

    results = retrieve_knowledge(query)

    print_results(results)