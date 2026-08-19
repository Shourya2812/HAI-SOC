"""
rag/evaluation/evaluator.py

RAG Evaluation & Grounding Engine for HAI-SOC.
Performs deterministic score calculation and rule validation for RAG-generated incident reports.
"""

import re
from dataclasses import dataclass, field
from typing import Any

from rag.evaluation.test_cases import RAGEvalTestCase, REQUIRED_HEADINGS_DEFAULT


@dataclass
class RAGEvalResult:
    test_case_id: str
    test_case_name: str
    passed: bool
    heading_score: float    # 0.0 to 1.0
    mitre_score: float      # 0.0 to 1.0
    nist_score: float       # 0.0 to 1.0
    hipaa_score: float      # 0.0 to 1.0
    grounding_score: float  # 0.0 to 1.0
    overall_score: float    # 0.0 to 1.0
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class RAGEvaluator:
    """
    Deterministic evaluator for HAI-SOC RAG incident reports.
    Compares generated report text against test case expected ground-truth requirements.
    """

    def __init__(self, required_headings: list[str] | None = None):
        self.required_headings = required_headings or REQUIRED_HEADINGS_DEFAULT

    def evaluate(self, test_case: RAGEvalTestCase, report_text: str) -> RAGEvalResult:
        failures: list[str] = []
        warnings: list[str] = []

        expected = test_case.expected
        source_log = test_case.mock_source_log

        # ------------------------------------------------------------
        # 1. Heading Validation
        # ------------------------------------------------------------
        found_headings = 0
        for heading in self.required_headings:
            if heading in report_text:
                found_headings += 1
            else:
                failures.append(f"Missing required section heading: '{heading}'")

        heading_score = found_headings / len(self.required_headings) if self.required_headings else 1.0

        # ------------------------------------------------------------
        # 2. MITRE Technique Validation (With Generic Subtechnique Parent-Child Matching)
        # ------------------------------------------------------------
        reported_mitre_ids = set(re.findall(r"T\d{4}(?:\.\d{3})?", report_text))

        mitre_failures = 0
        mitre_total_checks = len(expected.required_mitre) + len(expected.forbidden_mitre)

        # Check required MITRE IDs (matches exact ID or parent/subtechnique)
        for req_id in expected.required_mitre:
            matched_req = [m for m in reported_mitre_ids if m == req_id or m.startswith(req_id + ".")]
            if not matched_req:
                failures.append(f"Required MITRE technique missing: {req_id}")
                mitre_failures += 1

        # Check forbidden MITRE IDs (generic parent-child matching e.g. T1078 matches T1078.001)
        for forb_id in expected.forbidden_mitre:
            matched_forb = [m for m in reported_mitre_ids if m == forb_id or m.startswith(forb_id + ".")]
            if matched_forb:
                failures.append(f"Forbidden MITRE technique reported: {matched_forb[0]} (Forbidden parent: {forb_id})")
                mitre_failures += 1

        mitre_score = (mitre_total_checks - mitre_failures) / mitre_total_checks if mitre_total_checks > 0 else 1.0

        # ------------------------------------------------------------
        # 3. NIST Control Validation
        # ------------------------------------------------------------
        reported_nist_ids = set(re.findall(r"\b[A-Z]{2}-\d+(?:\(\d+\))?\b", report_text))
        nist_failures = 0
        nist_total_checks = len(expected.required_nist) + len(expected.forbidden_nist)

        for req_nist in expected.required_nist:
            if req_nist not in reported_nist_ids:
                failures.append(f"Required NIST control missing: {req_nist}")
                nist_failures += 1

        for forb_nist in expected.forbidden_nist:
            if forb_nist in reported_nist_ids:
                failures.append(f"Forbidden NIST control reported: {forb_nist}")
                nist_failures += 1

        fake_nist = re.findall(r"\b[A-Z]{2}\.\d+(?:\.\d+)?\b", report_text)
        if fake_nist:
            for fn in fake_nist:
                failures.append(f"Fabricated/Invalid NIST control format detected: {fn}")
                nist_failures += 1
                nist_total_checks += 1

        nist_score = (nist_total_checks - nist_failures) / nist_total_checks if nist_total_checks > 0 else 1.0

        # ------------------------------------------------------------
        # 4. HIPAA Breach Wording & Assessment Validation
        # ------------------------------------------------------------
        hipaa_score = 1.0
        if expected.must_not_claim_breach:
            conclusive_breach_terms = [
                "breach confirmed",
                "hipaa breach occurred",
                "confirmed hipaa breach",
                "guilty of a breach",
                "definitely violated hipaa",
                "this is a hipaa breach",
            ]
            report_lower = report_text.lower()
            for term in conclusive_breach_terms:
                if term in report_lower:
                    failures.append(f"Conclusive HIPAA breach claim detected ('{term}'). Report must use non-presumptive phrasing.")
                    hipaa_score = 0.0
                    break

        # ------------------------------------------------------------
        # 5. Grounding & Hallucination Validation (HARD GATE)
        # ------------------------------------------------------------
        grounding_failures = 0
        grounding_checks = 0

        actual_action = str(source_log.get("action", "")).upper()
        actual_user = str(source_log.get("user_id", ""))
        actual_dest = str(source_log.get("destination", ""))
        extra = source_log.get("extra", {})
        actual_failed_attempts = extra.get("failed_attempts", 0)

        # Extract ONLY OBSERVED EVIDENCE section from report
        obs_match = re.search(r"OBSERVED EVIDENCE\s*(.*?)\s*(?:IMPORTANT DATA DISCREPANCIES|WHY THE EVENT IS SUSPICIOUS|$)", report_text, re.DOTALL | re.IGNORECASE)
        obs_text = obs_match.group(1) if obs_match else report_text

        # Grounding Check 1: Event actions listed under OBSERVED EVIDENCE
        unobserved_actions = ["QUERY_DATABASE", "FILE_ACCESS", "NETWORK_CONNECTION", "DEVICE_TELEMETRY"]
        for unobs in unobserved_actions:
            if unobs != actual_action and unobs in obs_text:
                failures.append(f"GROUNDING FAILURE: Unobserved action '{unobs}' listed under OBSERVED EVIDENCE.")
                grounding_failures += 1
            grounding_checks += 1

        # Grounding Check 2: Invented user 'admin'
        if "admin" in obs_text.lower() and "admin" not in actual_user.lower() and "admin" not in str(source_log.get("role", "")).lower():
            failures.append("GROUNDING FAILURE: Invented user/role 'admin' listed under OBSERVED EVIDENCE.")
            grounding_failures += 1
        grounding_checks += 1

        # Grounding Check 3: Invented IP addresses in OBSERVED EVIDENCE
        ip_matches = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", obs_text)
        if ip_matches:
            failures.append(f"GROUNDING FAILURE: Invented IP address '{ip_matches[0]}' listed under OBSERVED EVIDENCE.")
            grounding_failures += 1
        grounding_checks += 1

        # Grounding Check 4: Data volume hallucinations (e.g. 50GB / Terabytes)
        actual_bytes = extra.get("bytes_sent", 0)
        if actual_bytes < 10000000:  # < 10MB
            if re.search(r"\b\d+\s*(?:gb|gigabyte|tb|terabyte)\b", report_text, re.IGNORECASE) or "thousands of records" in report_text.lower():
                failures.append("GROUNDING FAILURE: Massive data volume hallucination (e.g. GB/TB/thousands of records) detected.")
                grounding_failures += 1
        grounding_checks += 1

        # Grounding Check 5: Failed login attempts hallucination
        if actual_failed_attempts == 0:
            if "failed login attempts" in obs_text.lower() or "failed attempts" in obs_text.lower() or "brute force" in obs_text.lower():
                failures.append("GROUNDING FAILURE: Failed login attempts claimed under OBSERVED EVIDENCE when actual failed_attempts == 0.")
                grounding_failures += 1
        grounding_checks += 1

        grounding_score = (grounding_checks - grounding_failures) / grounding_checks if grounding_checks > 0 else 1.0

        # Authorization & Uncertainty Warnings
        if expected.must_require_authorization_check:
            report_lower = report_text.lower()
            if "authoriz" not in report_lower and "unknown" not in report_lower:
                warnings.append("Report did not explicitly mention authorization status verification under unknown / investigation.")

        # Overall Score Calculation with HARD GATE Grounding Penalty
        base_score = (heading_score * 0.20) + (mitre_score * 0.30) + (nist_score * 0.15) + (hipaa_score * 0.15) + (grounding_score * 0.20)
        overall_score = base_score * grounding_score  # Hard Gate: Grounding failure severely penalizes overall score

        passed = len(failures) == 0 and overall_score >= 0.85

        return RAGEvalResult(
            test_case_id=test_case.id,
            test_case_name=test_case.name,
            passed=passed,
            heading_score=round(heading_score, 4),
            mitre_score=round(mitre_score, 4),
            nist_score=round(nist_score, 4),
            hipaa_score=round(hipaa_score, 4),
            grounding_score=round(grounding_score, 4),
            overall_score=round(overall_score, 4),
            failures=failures,
            warnings=warnings,
        )

    def print_result(self, result: RAGEvalResult) -> None:
        status_str = "✅ PASSED" if result.passed else "❌ FAILED"
        print(f"\n{'='*70}")
        print(f"EVALUATION RESULT: [{result.test_case_id}] {result.test_case_name} — {status_str}")
        print(f"{'='*70}")
        print(f"Overall Score:    {result.overall_score * 100:.1f}%")
        print(f"  - Grounding:    {result.grounding_score * 100:.1f}%")
        print(f"  - Headings:     {result.heading_score * 100:.1f}%")
        print(f"  - MITRE:        {result.mitre_score * 100:.1f}%")
        print(f"  - NIST:         {result.nist_score * 100:.1f}%")
        print(f"  - HIPAA:        {result.hipaa_score * 100:.1f}%")

        if result.failures:
            print("\nFailures:")
            for f in result.failures:
                print(f"  ❌ {f}")

        if result.warnings:
            print("\nWarnings:")
            for w in result.warnings:
                print(f"  ⚠️ {w}")
        print(f"{'='*70}\n")
