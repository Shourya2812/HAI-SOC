"""
rag/evaluation/test_cases.py

RAG Evaluation Test Scenarios for HAI-SOC.
Defines 6 controlled test cases with telemetry baselines and ground-truth validation rules.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RAGEvalExpected:
    required_mitre: list[str] = field(default_factory=list)
    forbidden_mitre: list[str] = field(default_factory=list)
    required_nist: list[str] = field(default_factory=list)
    forbidden_nist: list[str] = field(default_factory=list)
    must_not_claim_breach: bool = True
    must_require_authorization_check: bool = False
    required_uncertainties: list[str] = field(default_factory=list)
    required_headings: list[str] = field(default_factory=list)


@dataclass
class RAGEvalTestCase:
    id: str
    name: str
    description: str
    incident: dict[str, Any]
    mock_source_log: dict[str, Any]
    expected: RAGEvalExpected


REQUIRED_HEADINGS_DEFAULT = [
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
# 6 CONTROLLED INCIDENT TEST SCENARIOS
# ============================================================

EVAL_TEST_CASES: list[RAGEvalTestCase] = [
    # ------------------------------------------------------------
    # TEST-01 — NORMAL PHI EXPORT
    # ------------------------------------------------------------
    RAGEvalTestCase(
        id="TEST-01",
        name="Normal PHI Export",
        description="Routine clinical PHI export by an authorized doctor during business hours.",
        incident={
            "title": "Security Anomaly: EXPORT_PHI",
            "description": "Low-volume PHI export logged in PACS.",
            "detector": "xgboost_v1",
            "anomaly_score": 0.120,
            "risk_level": "LOW",
            "log_id": "test_log_01",
        },
        mock_source_log={
            "id": "test_log_01",
            "timestamp": "2026-08-17 10:15:00",
            "source": "PACS",
            "destination": "PACS_Server",
            "user_id": "USR001",
            "role": "DOCTOR",
            "device": "WS-101",
            "department": "CARDIOLOGY",
            "action": "EXPORT_PHI",
            "severity": "LOW",
            "protocol": "HTTPS",
            "port": 443,
            "outcome": "SUCCESS",
            "extra": {
                "bytes_sent": 500000,
                "failed_attempts": 0,
                "unusual_hour": False,
                "records_accessed": 20,
                "mass_export": False,
            },
        },
        expected=RAGEvalExpected(
            required_mitre=[],
            forbidden_mitre=["T1002", "T1078", "T1567", "T1486"],
            forbidden_nist=["IR.12.4", "AU.99", "AC.999"],
            must_not_claim_breach=True,
            must_require_authorization_check=False,
            required_uncertainties=["Authorization status"],
            required_headings=REQUIRED_HEADINGS_DEFAULT,
        ),
    ),
    # ------------------------------------------------------------
    # TEST-02 — OFF-HOURS PHI EXPORT
    # ------------------------------------------------------------
    RAGEvalTestCase(
        id="TEST-02",
        name="Off-Hours PHI Export",
        description="Suspicious off-hours bulk export from PACS by IT personnel.",
        incident={
            "title": "Security Anomaly: EXPORT_PHI",
            "description": "Off-hours bulk export detected in PACS by xgboost_v1.",
            "detector": "xgboost_v1",
            "anomaly_score": 0.995,
            "risk_level": "CRITICAL",
            "log_id": "test_log_02",
        },
        mock_source_log={
            "id": "test_log_02",
            "timestamp": "2026-08-17 01:30:00",
            "source": "PACS",
            "destination": "PACS_Server",
            "user_id": "USR007",
            "role": "SOC_ANALYST",
            "device": "WS-039",
            "department": "IT",
            "action": "EXPORT_PHI",
            "severity": "MEDIUM",
            "protocol": "HTTPS",
            "port": 443,
            "outcome": "SUCCESS",
            "extra": {
                "bytes_sent": 5000000,
                "failed_attempts": 0,
                "unusual_hour": True,
                "records_accessed": 150,
                "mass_export": True,
            },
        },
        expected=RAGEvalExpected(
            required_mitre=[],
            forbidden_mitre=["T1002", "T1567", "T1486"],  # T1567 unconfirmed because destination is internal
            forbidden_nist=["IR.12.4", "AU.99", "AC.999"],
            must_not_claim_breach=True,
            must_require_authorization_check=True,
            required_uncertainties=["Authorization status"],
            required_headings=REQUIRED_HEADINGS_DEFAULT,
        ),
    ),
    # ------------------------------------------------------------
    # TEST-03 — AUTHENTICATION ANOMALY
    # ------------------------------------------------------------
    RAGEvalTestCase(
        id="TEST-03",
        name="Authentication Anomaly",
        description="Multiple failed login attempts followed by successful login during off-hours.",
        incident={
            "title": "Security Anomaly: LOGIN",
            "description": "Repeated authentication failures prior to success.",
            "detector": "isolation_forest_v1",
            "anomaly_score": 0.880,
            "risk_level": "HIGH",
            "log_id": "test_log_03",
        },
        mock_source_log={
            "id": "test_log_03",
            "timestamp": "2026-08-17 03:15:00",
            "source": "ActiveDirectory",
            "destination": "ActiveDirectory",
            "user_id": "USR009",
            "role": "NURSE",
            "device": "WS-088",
            "department": "EMERGENCY",
            "action": "LOGIN",
            "severity": "HIGH",
            "protocol": "HTTPS",
            "port": 443,
            "outcome": "SUCCESS",
            "extra": {
                "bytes_sent": 12000,
                "failed_attempts": 5,
                "unusual_hour": True,
                "records_accessed": 0,
                "mass_export": False,
            },
        },
        expected=RAGEvalExpected(
            required_mitre=["T1078"],
            forbidden_mitre=["T1567", "T1002", "T1486"],
            forbidden_nist=["IR.12.4", "AU.99", "AC.999"],
            must_not_claim_breach=True,
            must_require_authorization_check=True,
            required_uncertainties=["Credential compromise vs user error"],
            required_headings=REQUIRED_HEADINGS_DEFAULT,
        ),
    ),
    # ------------------------------------------------------------
    # TEST-04 — EXTERNAL WEB SERVICE EXFILTRATION
    # ------------------------------------------------------------
    RAGEvalTestCase(
        id="TEST-04",
        name="External Web Service Exfiltration",
        description="Mass PHI export routed directly to an unapproved external domain.",
        incident={
            "title": "Security Anomaly: EXPORT_PHI",
            "description": "Massive PHI export to external web service detected.",
            "detector": "xgboost_v1",
            "anomaly_score": 0.999,
            "risk_level": "CRITICAL",
            "log_id": "test_log_04",
        },
        mock_source_log={
            "id": "test_log_04",
            "timestamp": "2026-08-17 02:45:00",
            "source": "PACS",
            "destination": "external-web-service.example",
            "user_id": "USR003",
            "role": "RESEARCHER",
            "device": "WS-204",
            "department": "RESEARCH",
            "action": "EXPORT_PHI",
            "severity": "CRITICAL",
            "protocol": "HTTPS",
            "port": 443,
            "outcome": "SUCCESS",
            "extra": {
                "bytes_sent": 50000000,
                "failed_attempts": 0,
                "unusual_hour": True,
                "records_accessed": 500,
                "mass_export": True,
            },
        },
        expected=RAGEvalExpected(
            required_mitre=["T1567"],
            forbidden_mitre=["T1002", "T1486"],
            forbidden_nist=["IR.12.4", "AU.99", "AC.999"],
            must_not_claim_breach=True,
            must_require_authorization_check=True,
            required_uncertainties=["Destination reputational check"],
            required_headings=REQUIRED_HEADINGS_DEFAULT,
        ),
    ),
    # ------------------------------------------------------------
    # TEST-05 — RANSOMWARE
    # ------------------------------------------------------------
    RAGEvalTestCase(
        id="TEST-05",
        name="Ransomware Impact",
        description="High-frequency file modification with ransomware notes detected on PACS storage.",
        incident={
            "title": "Security Anomaly: FILE_ACCESS",
            "description": "High-volume file access and modification detected.",
            "detector": "xgboost_v1",
            "anomaly_score": 0.998,
            "risk_level": "CRITICAL",
            "log_id": "test_log_05",
        },
        mock_source_log={
            "id": "test_log_05",
            "timestamp": "2026-08-17 04:00:00",
            "source": "PACS",
            "destination": "PACS_Storage",
            "user_id": "USR012",
            "role": "SYSTEM_SERVICE",
            "device": "WS-012",
            "department": "IT",
            "action": "FILE_ACCESS",
            "severity": "CRITICAL",
            "protocol": "SMB",
            "port": 445,
            "outcome": "SUCCESS",
            "extra": {
                "bytes_sent": 85000000,
                "failed_attempts": 0,
                "unusual_hour": True,
                "records_accessed": 0,
                "mass_export": False,
                "encryption_activity": True,
                "files_modified": 12500,
                "ransom_note_detected": True,
            },
        },
        expected=RAGEvalExpected(
            required_mitre=["T1486"],
            forbidden_mitre=["T1567", "T1002"],
            forbidden_nist=["IR.12.4", "AU.99", "AC.999"],
            must_not_claim_breach=True,
            must_require_authorization_check=False,
            required_uncertainties=["Scope of compromised systems"],
            required_headings=REQUIRED_HEADINGS_DEFAULT,
        ),
    ),
    # ------------------------------------------------------------
    # TEST-06 — LARGE DATA TRANSFER WITHOUT COMPRESSION EVIDENCE
    # ------------------------------------------------------------
    RAGEvalTestCase(
        id="TEST-06",
        name="Large Data Transfer Without Compression",
        description="Large payload export to internal server without compression telemetry.",
        incident={
            "title": "Security Anomaly: EXPORT_PHI",
            "description": "Large payload PHI export to internal server.",
            "detector": "xgboost_v1",
            "anomaly_score": 0.960,
            "risk_level": "HIGH",
            "log_id": "test_log_06",
        },
        mock_source_log={
            "id": "test_log_06",
            "timestamp": "2026-08-17 05:20:00",
            "source": "PACS",
            "destination": "PACS_Server",
            "user_id": "USR005",
            "role": "RADIOLOGIST",
            "device": "WS-055",
            "department": "RADIOLOGY",
            "action": "EXPORT_PHI",
            "severity": "HIGH",
            "protocol": "HTTPS",
            "port": 443,
            "outcome": "SUCCESS",
            "extra": {
                "bytes_sent": 200000000,
                "failed_attempts": 0,
                "unusual_hour": True,
                "records_accessed": 1000,
                "mass_export": True,
                "compression_detected": False,
            },
        },
        expected=RAGEvalExpected(
            required_mitre=[],
            forbidden_mitre=["T1002", "T1567", "T1486"],  # T1002 MUST NOT be reported
            forbidden_nist=["IR.12.4", "AU.99", "AC.999"],
            must_not_claim_breach=True,
            must_require_authorization_check=True,
            required_uncertainties=["Authorization status"],
            required_headings=REQUIRED_HEADINGS_DEFAULT,
        ),
    ),
]
