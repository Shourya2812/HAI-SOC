"""
backend/app/services/incident_service.py

Business logic for healthcare security incidents and RAG AI report integration.
"""

import re
from datetime import UTC, datetime
from typing import Any

from bson import ObjectId

from backend.app.database.collections import (
    incidents_collection,
    logs_collection,
)
from backend.app.models.enums import (
    IncidentStatus,
    RiskLevel,
)
from backend.app.models.incident import Incident
from backend.app.schemas.incident_schema import (
    CreateIncidentRequest,
    IncidentResponse,
    UpdateIncidentRequest,
)


def parse_incident_report(raw_markdown: str) -> dict[str, Any]:
    """
    Deterministically parse the 11-section RAG incident report into structured fields.
    Extracts MITRE techniques, NIST controls, HIPAA impact, risk assessment,
    and recommended containment/investigation actions without secondary LLM calls.
    """
    now = datetime.now(UTC)
    parsed: dict[str, Any] = {
        "raw_markdown": raw_markdown,
        "generated_at": now,
        "mitre_techniques": [],
        "nist_controls": [],
        "hipaa_impact": None,
        "risk_assessment": None,
        "recommended_actions": [],
        "status": "GENERATED",
    }

    if not raw_markdown:
        return parsed

    # Helper to extract section content
    def get_section(name: str) -> str:
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
            + re.escape(name)
            + r"(?:\*\*)?:?\s*\n(.*?)(?=\n(?:\*\*|#+\s*)?(?:"
            + "|".join(re.escape(h) for h in headings)
            + r")(?:\*\*)?:?|\Z)"
        )
        match = re.search(pattern, raw_markdown, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    # 1. MITRE Techniques
    mitre_section = get_section("RELEVANT MITRE ATT&CK TECHNIQUES")
    if mitre_section and "No MITRE" not in mitre_section:
        tech_matches = re.findall(r"T\d{4}(?:\.\d{3})?", mitre_section)
        seen_techs = set()
        for t in tech_matches:
            if t not in seen_techs:
                parsed["mitre_techniques"].append(t)
                seen_techs.add(t)

    # 2. NIST Controls
    nist_section = get_section("RELEVANT NIST CONTROLS")
    if nist_section and "No specific NIST" not in nist_section:
        ctrl_matches = re.findall(r"\b[A-Z]{2}-\d+(?:\(\d+\))?\b", nist_section)
        seen_ctrls = set()
        for c in ctrl_matches:
            if c not in seen_ctrls:
                parsed["nist_controls"].append(c)
                seen_ctrls.add(c)

    # 3. HIPAA Impact
    hipaa_section = get_section("HIPAA IMPLICATIONS")
    if hipaa_section:
        parsed["hipaa_impact"] = hipaa_section

    # 4. Analyst Assessment / Risk
    assessment_section = get_section("ANALYST ASSESSMENT")
    if assessment_section:
        risk_match = re.search(r"Current Risk:\s*([A-Z]+)", assessment_section, re.IGNORECASE)
        if risk_match:
            parsed["risk_assessment"] = risk_match.group(1).upper()
        else:
            first_line = assessment_section.split("\n")[0].strip()
            parsed["risk_assessment"] = first_line if first_line else None

    # 5. Recommended Actions (Containment + Investigation)
    containment_section = get_section("RECOMMENDED CONTAINMENT ACTIONS")
    investigation_section = get_section("RECOMMENDED INVESTIGATION STEPS")

    actions = []
    for block in [containment_section, investigation_section]:
        if not block:
            continue
        for line in block.split("\n"):
            line_str = line.strip()
            clean_line = re.sub(r"^[-*•]\s+|\d+\.\s+", "", line_str).strip()
            if clean_line and len(clean_line) > 3 and not clean_line.startswith("#"):
                if clean_line not in actions:
                    actions.append(clean_line)

    parsed["recommended_actions"] = actions

    return parsed


class IncidentService:

    # --------------------------------------------------
    # Automatic Incident Creation (Primary Workflow)
    # --------------------------------------------------

    @staticmethod
    def create_from_prediction(
        *,
        log_id: str,
        detector: str,
        anomaly_score: float,
        title: str,
        description: str,
    ) -> IncidentResponse:

        if anomaly_score >= 0.90:
            risk = RiskLevel.CRITICAL
        elif anomaly_score >= 0.75:
            risk = RiskLevel.HIGH
        elif anomaly_score >= 0.50:
            risk = RiskLevel.MEDIUM
        else:
            risk = RiskLevel.LOW

        now = datetime.now(UTC)

        incident = Incident(
            title=title,
            description=description,
            log_id=log_id,
            detector=detector,
            anomaly_score=anomaly_score,
            risk_level=risk,
            status=IncidentStatus.OPEN,
            hipaa_impact=None,
            mitre_technique_id=None,
            report={},
            assigned_to=None,
            created_at=now,
            updated_at=now,
            resolved_at=None,
        )

        result = incidents_collection.insert_one(
            incident.model_dump()
        )

        return IncidentResponse(
            id=str(result.inserted_id),
            **incident.model_dump(),
        )

    # --------------------------------------------------
    # Manual Incident Creation (Optional)
    # --------------------------------------------------

    @staticmethod
    def create_incident(
        request: CreateIncidentRequest,
    ) -> IncidentResponse:

        now = datetime.now(UTC)

        incident = Incident(
            title=request.title,
            description=request.description,
            log_id=request.log_id,
            detector=request.detector,
            anomaly_score=request.anomaly_score,
            risk_level=request.risk_level,
            status=IncidentStatus.OPEN,
            hipaa_impact=request.hipaa_impact,
            mitre_technique_id=request.mitre_technique_id,
            report=request.report,
            assigned_to=request.assigned_to,
            created_at=now,
            updated_at=now,
            resolved_at=None,
        )

        result = incidents_collection.insert_one(
            incident.model_dump()
        )

        return IncidentResponse(
            id=str(result.inserted_id),
            **incident.model_dump(),
        )

    @staticmethod
    def get_incident(
        incident_id: str,
    ):
        try:
            inc_obj_id = ObjectId(incident_id)
        except Exception:
            return None

        document = incidents_collection.find_one(
            {
                "_id": inc_obj_id
            }
        )

        if document is None:
            return None

        document["id"] = str(document["_id"])
        document.pop("_id")

        return IncidentResponse(**document)

    @staticmethod
    def get_incidents():

        incidents = []

        for document in incidents_collection.find():

            document["id"] = str(document["_id"])
            document.pop("_id")

            incidents.append(
                IncidentResponse(**document)
            )

        return incidents

    @staticmethod
    def update_incident(
        incident_id: str,
        request: UpdateIncidentRequest,
    ):
        try:
            inc_obj_id = ObjectId(incident_id)
        except Exception:
            return None

        update_data = request.model_dump(
            exclude_none=True
        )

        update_data["updated_at"] = datetime.now(UTC)

        incidents_collection.update_one(
            {
                "_id": inc_obj_id
            },
            {
                "$set": update_data
            }
        )

        return IncidentService.get_incident(
            incident_id
        )

    @staticmethod
    def delete_incident(
        incident_id: str,
    ):
        try:
            inc_obj_id = ObjectId(incident_id)
        except Exception:
            return False

        result = incidents_collection.delete_one(
            {
                "_id": inc_obj_id
            }
        )

        return result.deleted_count == 1

    # --------------------------------------------------
    # RAG Incident Investigation Report Generation (Phase R11)
    # --------------------------------------------------

    @staticmethod
    def generate_incident_report(
        incident_id: str,
    ) -> IncidentResponse:
        """
        Generate a grounded RAG incident report for an existing incident.
        Orchestrates MongoDB retrieval, RAG analysis invocation, deterministic parsing,
        and persistence of the report back into MongoDB.
        """
        from rag.generator import analyze_incident

        try:
            inc_obj_id = ObjectId(incident_id)
        except Exception:
            raise ValueError(f"Invalid incident ID format: {incident_id}")

        incident_doc = incidents_collection.find_one({"_id": inc_obj_id})
        if not incident_doc:
            raise ValueError(f"Incident not found: {incident_id}")

        log_id = incident_doc.get("log_id")
        if not log_id:
            raise ValueError(f"Incident {incident_id} has no associated log_id")

        # Retrieve authoritative source log
        source_log = None
        try:
            log_obj_id = ObjectId(log_id)
            source_log = logs_collection.find_one({"_id": log_obj_id})
        except Exception:
            pass

        if not source_log:
            source_log = logs_collection.find_one({"id": log_id})

        if not source_log:
            raise ValueError(f"Authoritative source log not found for incident {incident_id} (log_id={log_id})")

        # Build incident dictionary matching rag.generator boundary
        incident_dict = {
            "title": incident_doc.get("title", "Security Incident"),
            "description": incident_doc.get("description", ""),
            "detector": incident_doc.get("detector", ""),
            "anomaly_score": incident_doc.get("anomaly_score", 0.0),
            "risk_level": str(incident_doc.get("risk_level", "LOW")),
            "log_id": str(log_id),
        }

        # Invoke frozen RAG generator (Single Ollama LLM call)
        raw_report = analyze_incident(incident=incident_dict, source_log=source_log)

        # Deterministic parsing of report sections
        parsed_report = parse_incident_report(raw_report)

        now = datetime.now(UTC)
        update_fields: dict[str, Any] = {
            "report": parsed_report,
            "updated_at": now,
        }

        primary_mitre = parsed_report["mitre_techniques"][0] if parsed_report["mitre_techniques"] else None
        if primary_mitre:
            update_fields["mitre_technique_id"] = primary_mitre

        hipaa_impact = parsed_report.get("hipaa_impact")
        if hipaa_impact:
            update_fields["hipaa_impact"] = hipaa_impact

        incidents_collection.update_one(
            {"_id": inc_obj_id},
            {"$set": update_fields}
        )

        return IncidentService.get_incident(incident_id)