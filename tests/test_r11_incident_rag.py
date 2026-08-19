"""
tests/test_r11_incident_rag.py

Unit and integration tests for Phase R11:
- Deterministic RAG report parser
- Incident Service report generation and persistence
- FastAPI /incidents/{incident_id}/analyze endpoint
- Backward compatibility for existing report: {} structures
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, UTC
from bson import ObjectId

from backend.app.services.incident_service import parse_incident_report, IncidentService
from backend.app.schemas.incident_schema import IncidentResponse, IncidentReportSchema
from backend.app.models.enums import IncidentStatus, RiskLevel


SAMPLE_RAG_REPORT = """INCIDENT SUMMARY

A critical security event was observed where a researcher (USR003) attempted to export patient records (EXPORT_PHI) to an external web service (external-web-service.example). The export involved 50 million bytes and 500 records.

OBSERVED EVIDENCE

- log_id: test_log_04
- timestamp: 2026-08-17 02:45:00
- source: PACS
- destination: external-web-service.example
- user_id: USR003
- role: RESEARCHER
- department: RESEARCH
- action: EXPORT_PHI
- severity: CRITICAL
- outcome: SUCCESS
- extra.bytes_sent: 50000000

IMPORTANT DATA DISCREPANCIES

No discrepancies identified.

WHY THE EVENT IS SUSPICIOUS

High volume PHI transfer to an unapproved external destination during off-hours.

UNKNOWN / REQUIRES INVESTIGATION

- Verify if researcher USR003 has an approved clinical transfer ticket.
- Perform WHOIS lookup on external-web-service.example.

HIPAA IMPLICATIONS

May require HIPAA breach assessment. Potential unencrypted ePHI disclosure of 500 patient records under 45 CFR § 164.402.

RELEVANT MITRE ATT&CK TECHNIQUES

- Exfiltration Over Web Service (T1567): Data exported over HTTPS to external web service.

RELEVANT NIST CONTROLS

- AC-3: Access Enforcement
- AU-6: Audit Record Review, Analysis, and Reporting

RECOMMENDED INVESTIGATION STEPS

1. Verify user USR003 data export authorizations with Research Director.
2. Inspect PACS audit logs for concurrent export activity.

RECOMMENDED CONTAINMENT ACTIONS

1. Block outbound traffic to destination external-web-service.example at perimeter firewall.
2. Temporarily revoke PACS export permissions for user USR003.

ANALYST ASSESSMENT

Current Risk: CRITICAL
Strongest Evidence: 500 patient records transferred to external web service.
Major Uncertainty: User authorization status.
Immediate Next Action: Block external destination and isolate account.
"""


class TestR11DeterministicParser(unittest.TestCase):
    """Test the deterministic RAG report parser."""

    def test_parse_valid_report(self):
        parsed = parse_incident_report(SAMPLE_RAG_REPORT)

        self.assertEqual(parsed["raw_markdown"], SAMPLE_RAG_REPORT)
        self.assertEqual(parsed["status"], "GENERATED")
        self.assertIsInstance(parsed["generated_at"], datetime)

        # MITRE techniques extraction
        self.assertIn("T1567", parsed["mitre_techniques"])

        # NIST controls extraction
        self.assertIn("AC-3", parsed["nist_controls"])
        self.assertIn("AU-6", parsed["nist_controls"])

        # HIPAA implications
        self.assertIsNotNone(parsed["hipaa_impact"])
        self.assertIn("HIPAA breach assessment", parsed["hipaa_impact"])

        # Risk assessment
        self.assertEqual(parsed["risk_assessment"], "CRITICAL")

        # Actions (containment + investigation)
        self.assertTrue(len(parsed["recommended_actions"]) >= 4)
        self.assertTrue(any("Block outbound traffic" in act for act in parsed["recommended_actions"]))
        self.assertTrue(any("Verify user USR003" in act for act in parsed["recommended_actions"]))

    def test_parse_empty_report(self):
        parsed = parse_incident_report("")
        self.assertEqual(parsed["raw_markdown"], "")
        self.assertEqual(parsed["mitre_techniques"], [])
        self.assertEqual(parsed["nist_controls"], [])
        self.assertIsNone(parsed["hipaa_impact"])
        self.assertEqual(parsed["recommended_actions"], [])

    def test_parse_report_without_mitre(self):
        report_no_mitre = """INCIDENT SUMMARY
Routine export.

RELEVANT MITRE ATT&CK TECHNIQUES
No MITRE ATT&CK technique can be confidently identified from the available evidence.

RELEVANT NIST CONTROLS
No specific NIST control confidently mapped from retrieved knowledge.
"""
        parsed = parse_incident_report(report_no_mitre)
        self.assertEqual(parsed["mitre_techniques"], [])
        self.assertEqual(parsed["nist_controls"], [])


class TestR11IncidentService(unittest.TestCase):
    """Test IncidentService integration and error handling."""

    @patch("backend.app.services.incident_service.incidents_collection")
    @patch("backend.app.services.incident_service.logs_collection")
    def test_generate_incident_report_nonexistent_incident(self, mock_logs, mock_incidents):
        mock_incidents.find_one.return_value = None

        with self.assertRaises(ValueError) as ctx:
            IncidentService.generate_incident_report("507f1f77bcf86cd799439011")

        self.assertIn("not found", str(ctx.exception).lower())

    @patch("backend.app.services.incident_service.incidents_collection")
    @patch("backend.app.services.incident_service.logs_collection")
    def test_generate_incident_report_missing_source_log(self, mock_logs, mock_incidents):
        mock_incidents.find_one.return_value = {
            "_id": ObjectId("507f1f77bcf86cd799439011"),
            "log_id": "nonexistent_log_123",
            "title": "Test Incident",
        }
        mock_logs.find_one.return_value = None

        with self.assertRaises(ValueError) as ctx:
            IncidentService.generate_incident_report("507f1f77bcf86cd799439011")

        self.assertIn("source log not found", str(ctx.exception).lower())

    @patch("rag.generator.analyze_incident")
    @patch("backend.app.services.incident_service.incidents_collection")
    @patch("backend.app.services.incident_service.logs_collection")
    def test_generate_incident_report_success(self, mock_logs, mock_incidents, mock_analyze):
        mock_analyze.return_value = SAMPLE_RAG_REPORT

        inc_id = ObjectId("507f1f77bcf86cd799439011")
        log_id = ObjectId("507f1f77bcf86cd799439022")

        mock_incidents.find_one.side_effect = [
            # First lookup before generation
            {
                "_id": inc_id,
                "log_id": str(log_id),
                "title": "Security Anomaly: EXPORT_PHI",
                "description": "Anomalous export detected.",
                "detector": "xgboost_v1",
                "anomaly_score": 0.999,
                "risk_level": "CRITICAL",
                "status": "OPEN",
                "report": {},
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC),
            },
            # Second lookup by get_incident after update
            {
                "_id": inc_id,
                "log_id": str(log_id),
                "title": "Security Anomaly: EXPORT_PHI",
                "description": "Anomalous export detected.",
                "detector": "xgboost_v1",
                "anomaly_score": 0.999,
                "risk_level": "CRITICAL",
                "status": "OPEN",
                "mitre_technique_id": "T1567",
                "hipaa_impact": "May require HIPAA breach assessment.",
                "report": {
                    "raw_markdown": SAMPLE_RAG_REPORT,
                    "generated_at": datetime.now(UTC),
                    "mitre_techniques": ["T1567"],
                    "nist_controls": ["AC-3", "AU-6"],
                    "status": "GENERATED",
                },
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC),
            },
        ]

        mock_logs.find_one.return_value = {
            "_id": log_id,
            "id": "test_log_04",
            "action": "EXPORT_PHI",
            "source": "PACS",
            "destination": "external-web-service.example",
            "user_id": "USR003",
        }

        result = IncidentService.generate_incident_report(str(inc_id))

        self.assertIsNotNone(result)
        self.assertEqual(result.mitre_technique_id, "T1567")
        techniques = result.report.mitre_techniques if hasattr(result.report, "mitre_techniques") else result.report.get("mitre_techniques", [])
        self.assertIn("T1567", techniques)
        mock_analyze.assert_called_once()
        mock_incidents.update_one.assert_called_once()


if __name__ == "__main__":
    unittest.main()
