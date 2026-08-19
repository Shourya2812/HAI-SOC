"""
rag/generator.py

RAG-powered healthcare security incident analysis.

Pipeline:
Incident → Authoritative Source Log → Fact Extraction & Absent Evidence → Qdrant Retrieval → Grounded Prompt → Qwen → Validation → SOC Report
"""

import re
from typing import Any

from rag.incident_query import (
    build_incident_query,
    get_source_log,
)
from rag.llm import generate_response
from rag.retriever import retrieve_knowledge
from rag.mongo_incident import get_incident_with_source_log


# ============================================================
# REQUIRED HEADINGS CONTRACT
# ============================================================

REQUIRED_HEADINGS = [
    "INCIDENT SUMMARY",
    "OBSERVED EVIDENCE",
    "IMPORTANT DATA DISCREPANCIES",
    "WHY THE EVENT IS SUSPICIOUS",
    "UNKNOWN / REQUIRES INVESTIGATION",
    "HIPAA IMPLICATIONS",
    "RELEVANT MITRE ATT&CK TECHNIQUES",
    "RELEVANT NIST CONTROLS",
    "RECOMMENDED INVESTIGATION STEPS",
    "RECOMMENDED CONTAINMENT ACTIONS",
    "ANALYST ASSESSMENT",
]


# ============================================================
# 1. AUTHORITATIVE FACT BLOCK
# ============================================================

def build_authoritative_facts(source_log: dict[str, Any] | None) -> str:
    """
    Produce a compact, unambiguous factual representation of observed telemetry.
    THIS IS THE ONLY SOURCE OF OBSERVED FACTUAL TELEMETRY.
    """
    if not source_log:
        return "AUTHORITATIVE OBSERVED FACTS: NONE (Source log unavailable)."

    extra = source_log.get("extra", {})

    facts = [
        "AUTHORITATIVE OBSERVED FACTS (SOURCE LOG TELEMETRY):",
        f"- log_id: {source_log.get('id', source_log.get('_id'))}",
        f"- action: {source_log.get('action')}",
        f"- severity: {source_log.get('severity')}",
        f"- outcome: {source_log.get('outcome')}",
        f"- user_id: {source_log.get('user_id')}",
        f"- role: {source_log.get('role')}",
        f"- department: {source_log.get('department')}",
        f"- source: {source_log.get('source')}",
        f"- destination: {source_log.get('destination')}",
        f"- device: {source_log.get('device')}",
        f"- protocol: {source_log.get('protocol')}",
        f"- port: {source_log.get('port')}",
        f"- timestamp: {source_log.get('timestamp')}",
    ]

    for key, val in extra.items():
        facts.append(f"- {key}: {val}")

    return "\n".join(facts)


# ============================================================
# 2. NEGATIVE / ABSENT EVIDENCE BLOCK
# ============================================================

def build_absent_evidence(source_log: dict[str, Any] | None) -> str:
    """
    Construct an explicit negative evidence block stating what was NOT observed.
    Prevents the LLM from taking examples from RAG reference documents and treating them as observed telemetry.
    """
    if not source_log:
        return "ABSENT / UNSUPPORTED EVENTS: Source log unavailable."

    action = str(source_log.get("action", "")).upper()
    destination = str(source_log.get("destination", ""))
    extra = source_log.get("extra", {})
    failed_attempts = extra.get("failed_attempts", 0)

    absent = [
        "ABSENT / UNSUPPORTED EVENTS (DO NOT INVENT OR CLAIM IN REPORT):"
    ]

    if action != "LOGIN" and failed_attempts == 0:
        absent.append("- No failed login attempts, authentication failures, credential brute force, or password spraying observed.")

    if action != "QUERY_DATABASE":
        absent.append("- No QUERY_DATABASE or backend SQL query execution observed.")

    if action != "FILE_ACCESS" and not extra.get("encryption_activity", False):
        absent.append("- No FILE_ACCESS, ransomware file modifications, file encryption, or ransom notes observed.")

    if action != "NETWORK_CONNECTION":
        absent.append("- No NETWORK_CONNECTION, lateral subnet movement, or C2 network traffic observed.")

    if action != "DEVICE_TELEMETRY":
        absent.append("- No DEVICE_TELEMETRY or IoMT medical device disruptions observed.")

    # Check external destination
    if not (destination.startswith("http://") or destination.startswith("https://") or ("." in destination and "Server" not in destination and "DB" not in destination and "Storage" not in destination and "PACS" not in destination and "ActiveDirectory" not in destination)):
        absent.append("- No external web destination, cloud storage upload, or external IP traversal observed (destination is internal).")

    if not extra.get("compression_detected", False):
        absent.append("- No data compression, archive creation (zip, 7z, rar), or compression telemetry observed.")

    return "\n".join(absent)


# ============================================================
# 3. CATEGORY-AWARE RAG CONTEXT BUILDER
# ============================================================

def build_rag_context(results: list[dict[str, Any]]) -> str:
    """
    Convert retrieved Qdrant results into category-filtered reference blocks.
    Retrieved knowledge is REFERENCE MATERIAL ONLY.
    It MUST NOT be used to invent observed telemetry events.
    """
    if not results:
        return "NO RETRIEVED REFERENCE KNOWLEDGE FOUND."

    by_category: dict[str, list[dict[str, Any]]] = {
        "HIPAA": [],
        "NIST": [],
        "MITRE": [],
        "RUNBOOK": [],
        "OTHER": [],
    }

    for item in results:
        cat = str(item.get("category", "")).upper()
        if "HIPAA" in cat:
            by_category["HIPAA"].append(item)
        elif "NIST" in cat:
            by_category["NIST"].append(item)
        elif "MITRE" in cat:
            by_category["MITRE"].append(item)
        elif "RUNBOOK" in cat:
            by_category["RUNBOOK"].append(item)
        else:
            by_category["OTHER"].append(item)

    sections = []

    for cat_name, items in by_category.items():
        if not items:
            continue
        header = f"=== {cat_name} REFERENCE MATERIAL (GUIDANCE ONLY — NOT OBSERVED EVENTS) ==="
        chunks = []
        for idx, item in enumerate(items, start=1):
            chunks.append(
                f"[{cat_name} Doc {idx}] Title: {item.get('title')}\n"
                f"Document ID: {item.get('document_id')}\n"
                f"Content Summary: {item.get('text', '')}"
            )
        sections.append(header + "\n" + "\n\n".join(chunks))

    return "\n\n".join(sections)

def build_observed_evidence(source_log: dict) -> str:
    """
    Build the OBSERVED EVIDENCE section deterministically.

    This section MUST NOT be generated by the LLM.
    """
    lines = [
        f"- log_id: {source_log.get('id') or source_log.get('_id')}",
        f"- timestamp: {source_log.get('timestamp')}",
        f"- source: {source_log.get('source')}",
        f"- destination: {source_log.get('destination')}",
        f"- user_id: {source_log.get('user_id')}",
        f"- role: {source_log.get('role')}",
        f"- device: {source_log.get('device')}",
        f"- department: {source_log.get('department')}",
        f"- action: {source_log.get('action')}",
        f"- severity: {source_log.get('severity')}",
        f"- protocol: {source_log.get('protocol')}",
        f"- port: {source_log.get('port')}",
        f"- outcome: {source_log.get('outcome')}",
    ]
    extra = source_log.get("extra") or {}
    for k, v in extra.items():
        lines.append(f"- extra.{k}: {v}")

    return "OBSERVED EVIDENCE\n\n" + "\n".join(lines)


# ============================================================
# 4. RAG PROMPT BUILDER
# ============================================================

def build_rag_prompt(
    incident: dict,
    context: str,
    source_log: dict | None = None,
) -> str:
    """
    Build an analysis-only prompt.

    The LLM does NOT generate authoritative telemetry.
    """

    if source_log is None:
        raise ValueError(
            "source_log is required for grounded analysis"
        )

    extra = source_log.get("extra") or {}

    return f"""
You are an expert healthcare SOC analyst.

Your task is to ANALYZE the security event below.

You are NOT responsible for reproducing the telemetry.

The telemetry is authoritative and has already been extracted
by the HAI-SOC application.

============================================================
AUTHORITATIVE EVENT
============================================================

Action: {source_log.get("action")}
Severity: {source_log.get("severity")}
Outcome: {source_log.get("outcome")}
User ID: {source_log.get("user_id")}
Role: {source_log.get("role")}
Department: {source_log.get("department")}
Source: {source_log.get("source")}
Destination: {source_log.get("destination")}
Device: {source_log.get("device")}
Protocol: {source_log.get("protocol")}
Port: {source_log.get("port")}
Timestamp: {source_log.get("timestamp")}

bytes_sent: {extra.get("bytes_sent")}
failed_attempts: {extra.get("failed_attempts")}
unusual_hour: {extra.get("unusual_hour")}
records_accessed: {extra.get("records_accessed")}

============================================================
IMPORTANT
============================================================

Treat the AUTHORITATIVE EVENT above as the ONLY factual
description of what happened.

Do NOT invent:

- users
- IP addresses
- domains
- destinations
- records
- bytes
- login events
- file events
- ransomware
- malware
- C2
- lateral movement
- compression
- cloud storage
- authorization status
- change tickets
- threat intelligence results

If something is not present in the authoritative event,
say that it requires investigation.

The destination is:

{source_log.get("destination")}

Do NOT describe it as external unless the telemetry explicitly
establishes that it is external.

============================================================
RETRIEVED SECURITY KNOWLEDGE
============================================================

The following material provides cybersecurity, HIPAA, NIST,
MITRE, and healthcare incident-response guidance.

It is NOT evidence of what happened.

{context}

============================================================
ANALYSIS TASK
============================================================

Generate ONLY the following sections:

INCIDENT SUMMARY

WHY THE EVENT IS SUSPICIOUS

UNKNOWN / REQUIRES INVESTIGATION

HIPAA IMPLICATIONS

RELEVANT MITRE ATT&CK TECHNIQUES

RELEVANT NIST CONTROLS

RECOMMENDED INVESTIGATION STEPS

RECOMMENDED CONTAINMENT ACTIONS

ANALYST ASSESSMENT

============================================================
MITRE RULES
============================================================

Only identify a MITRE technique when the authoritative telemetry
supports it.

T1486:
Only if explicit encryption activity or ransom-note evidence
exists.

T1567:
Only if the authoritative telemetry explicitly establishes
an external web-service destination.

T1078:
Only if the telemetry explicitly supports valid-account misuse
or the relevant authentication scenario.

T1002:
NEVER infer compression from bytes_sent.

If no technique is sufficiently supported, say:

"No MITRE ATT&CK technique can be confidently identified from
the available evidence."

============================================================
HIPAA RULE
============================================================

Do NOT declare that a HIPAA breach occurred.

Use language such as:

"May require HIPAA breach assessment."

============================================================
NIST RULE
============================================================

Only reference controls supported by the retrieved NIST
material.

============================================================
ANALYST ASSESSMENT
============================================================

Use exactly:

Current Risk:
Strongest Evidence:
Major Uncertainty:
Immediate Next Action:

Return ONLY the requested analysis sections.
""".strip()


# ============================================================
# PROGRAMMATIC SAFETY & VALIDATION
# ============================================================

def validate_response(response: str, results: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Perform lightweight programmatic safety validation on LLM output.
    """
    validation_summary = {
        "missing_headings": [],
        "unsupported_mitre": [],
        "unsupported_nist": [],
    }

    for heading in REQUIRED_HEADINGS:
        if heading not in response:
            validation_summary["missing_headings"].append(heading)
            print(f"[WARNING] Missing required heading in report: '{heading}'")

    retrieved_mitre_ids = set()
    retrieved_nist_ids = set()

    for item in results:
        text = item.get("text", "")
        doc_id = item.get("document_id", "")
        title = item.get("title", "")
        combined = f"{doc_id} {title} {text}"

        mitre_matches = re.findall(r"T\d{4}(?:\.\d{3})?", combined)
        retrieved_mitre_ids.update(mitre_matches)

        nist_matches = re.findall(r"\b[A-Z]{2}-\d+(?:\(\d+\))?\b", combined)
        retrieved_nist_ids.update(nist_matches)

    response_mitre = set(re.findall(r"T\d{4}(?:\.\d{3})?", response))
    for tech_id in response_mitre:
        base_id = tech_id.split(".")[0]
        if tech_id not in retrieved_mitre_ids and base_id not in retrieved_mitre_ids:
            validation_summary["unsupported_mitre"].append(tech_id)
            print(f"[WARNING] Potential unsupported MITRE technique in LLM response: {tech_id}")

    response_nist = set(re.findall(r"\b[A-Z]{2}-\d+(?:\(\d+\))?\b", response))
    for ctrl_id in response_nist:
        if ctrl_id not in retrieved_nist_ids:
            validation_summary["unsupported_nist"].append(ctrl_id)
            print(f"[WARNING] Potential unsupported NIST control in LLM response: {ctrl_id}")

    return validation_summary


# ============================================================
# COMPLETE RAG PIPELINE
# ============================================================

def build_incident_from_mongodb(
    incident_id: str,
) -> tuple[dict, dict]:
    """
    Load an HAI-SOC incident and its authoritative
    source log from MongoDB.

    Returns:
        incident:
            Normalized incident metadata used by RAG.

        source_log:
            Authoritative MongoDB security event.
    """

    result = get_incident_with_source_log(
        incident_id
    )

    if result is None:
        raise ValueError(
            f"Incident not found: {incident_id}"
        )

    mongo_incident = result["incident"]
    source_log = result["source_log"]

    incident = {
        "title": mongo_incident.get(
            "title",
            "Security Incident",
        ),

        "description": mongo_incident.get(
            "description",
            "",
        ),

        "detector": mongo_incident.get(
            "detector",
            "",
        ),

        "anomaly_score": mongo_incident.get(
            "anomaly_score",
            "",
        ),

        "risk_level": mongo_incident.get(
            "risk_level",
            "",
        ),

        "log_id": mongo_incident.get(
            "log_id",
            "",
        ),
    }

    return incident, source_log


def extract_section(
    text: str,
    heading: str,
) -> str:
    """
    Extract the content under a specific section heading from LLM response.
    """
    headings = [
        "INCIDENT SUMMARY",
        "OBSERVED EVIDENCE",
        "IMPORTANT DATA DISCREPANCIES",
        "WHY THE EVENT IS SUSPICIOUS",
        "UNKNOWN / REQUIRES INVESTIGATION",
        "HIPAA IMPLICATIONS",
        "RELEVANT MITRE ATT&CK TECHNIQUES",
        "RELEVANT NIST CONTROLS",
        "RECOMMENDED INVESTIGATION STEPS",
        "RECOMMENDED CONTAINMENT ACTIONS",
        "ANALYST ASSESSMENT",
    ]
    pattern = (
        r"(?:^|\n)(?:\*\*|#+\s*)?"
        + re.escape(heading)
        + r"(?:\*\*)?:?\s*\n(.*?)(?=\n(?:\*\*|#+\s*)?(?:"
        + "|".join(re.escape(h) for h in headings)
        + r")(?:\*\*)?:?|\Z)"
    )
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""


def analyze_incident(
    incident: dict,
    source_log: dict | None = None,
) -> str:
    """
    Execute the grounded RAG pipeline.
    """

    if source_log is None:
        raise ValueError(
            "Authoritative source_log is required"
        )

    # ---------------------------------------------------------
    # 1. Build retrieval query
    # ---------------------------------------------------------

    query = build_incident_query(
        incident
    )

    # ---------------------------------------------------------
    # 2. Retrieve healthcare security knowledge
    # ---------------------------------------------------------

    results = retrieve_knowledge(
        query,
        results_per_collection=3,
    )

    context = build_rag_context(
        results
    )

    # ---------------------------------------------------------
    # 3. Build analysis-only prompt
    # ---------------------------------------------------------

    prompt = build_rag_prompt(
        incident=incident,
        context=context,
        source_log=source_log,
    )

    # ---------------------------------------------------------
    # 4. Ask Qwen for ANALYSIS ONLY
    # ---------------------------------------------------------

    response = generate_response(
        prompt
    )

    # ---------------------------------------------------------
    # 5. Build authoritative evidence deterministically
    # ---------------------------------------------------------

    observed_evidence = build_observed_evidence(
        source_log
    )

    # ---------------------------------------------------------
    # 6. Build final report
    # ---------------------------------------------------------

    final_report = f"""
INCIDENT SUMMARY

{extract_section(response, "INCIDENT SUMMARY")}

{observed_evidence}

IMPORTANT DATA DISCREPANCIES

No discrepancies identified between the authoritative MongoDB source log and incident metadata.

WHY THE EVENT IS SUSPICIOUS

{extract_section(response, "WHY THE EVENT IS SUSPICIOUS")}

UNKNOWN / REQUIRES INVESTIGATION

{extract_section(response, "UNKNOWN / REQUIRES INVESTIGATION")}

HIPAA IMPLICATIONS

{extract_section(response, "HIPAA IMPLICATIONS")}

RELEVANT MITRE ATT&CK TECHNIQUES

{extract_section(response, "RELEVANT MITRE ATT&CK TECHNIQUES")}

RELEVANT NIST CONTROLS

{extract_section(response, "RELEVANT NIST CONTROLS")}

RECOMMENDED INVESTIGATION STEPS

{extract_section(response, "RECOMMENDED INVESTIGATION STEPS")}

RECOMMENDED CONTAINMENT ACTIONS

{extract_section(response, "RECOMMENDED CONTAINMENT ACTIONS")}

ANALYST ASSESSMENT

{extract_section(response, "ANALYST ASSESSMENT")}
""".strip()

    return final_report


# ============================================================
# TEST EXECUTION
# ============================================================

if __name__ == "__main__":

    INCIDENT_ID = "6a80c6b1c091aba98edbbc23"

    print(
        "\nGenerating RAG-powered incident analysis...\n"
    )

    incident, source_log = build_incident_from_mongodb(
        INCIDENT_ID
    )

    response = analyze_incident(
        incident=incident,
        source_log=source_log,
    )

    print("\n")
    print("=" * 80)
    print("HAI-SOC AI INCIDENT REPORT")
    print("=" * 80)
    print()

    print(response)

    print("=" * 80)