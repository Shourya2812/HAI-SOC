---
document_id: runbook-credential-theft-v1
category: RUNBOOK
framework: INTERNAL_RUNBOOK
title: Credential Theft / Account Compromise Response Runbook
source: HAI-SOC
citation: HAI-SOC Internal Runbook
trigger_event: LOGIN
severity_level: HIGH
affected_assets:
  - ActiveDirectory
  - EHR
  - VPN
tags:
  - runbook
  - credential_theft
  - account_compromise
  - login_anomaly
  - brute_force
  - mitre_t1078
---

# Credential Theft / Account Compromise Response Runbook

## Purpose

This operational runbook provides a standardized incident response sequence for SOC analysts investigating potential credential theft, brute-force authentication, or stolen account abuse within the HAI-SOC platform.

## Trigger Conditions

An investigation under this runbook is triggered when the ML anomaly pipeline (`xgboost_v1`, `isolation_forest_v1`) flags an authentication event crossing anomaly threshold ($\ge 0.50$), featuring one or more of the following HAI-SOC log schema indicators:

- **Primary Action:** `action == "LOGIN"` or `action == "API_REQUEST"`
- **Authentication Failures:** `outcome == "FAILURE"` with `extra.failed_attempts > 0`
- **Successful Login Following Failures:** `outcome == "SUCCESS"` recorded immediately following a burst of `extra.failed_attempts` for the same `user_id`.
- **Timing & Location:** `extra.unusual_hour == True` or unexpected `source` system (e.g. `VPN`, `IoMT`, `API_Gateway`).
- **Device Anomaly:** `device` workstation associated with `user_id` deviates from historical device usage baselines.

## Initial Triage

SOC analysts should execute the following 6-step initial triage sequence:

1. **Validate Identity:** Confirm the identity and employment status of `user_id` in Active Directory.
2. **Review Authentication History:** Examine prior `LOGIN` events for `user_id` across the preceding 7 days to identify normal vs. abnormal login windows.
3. **Review Device History:** Verify whether the requesting `device` workstation is an authorized healthcare endpoint assigned to `user_id`.
4. **Review Network Source Evidence:** Inspect `source`, `destination`, `protocol`, and `port` to verify subnet traversal paths.
5. **Determine Privileged Access:** Check whether `role` includes administrative or elevated access permissions (e.g., `ADMIN`, `IT`, `SOC_ANALYST`).
6. **Check Subsequent Actions:** Query `logs_collection` for all actions performed by `user_id` immediately following the successful authentication event (e.g. subsequent `EXPORT_PHI` or `QUERY_DATABASE` calls).

## Evidence Collection

- Preserve all `LOGIN` and `API_REQUEST` log records (`log_id`) associated with the authentication session.
- Export ML anomaly score details (`anomaly_score`, `detector`) from `anomaly_scores`.
- Extract failure count statistics (`extra.failed_attempts`) and timestamp deltas.
- *(Future Evidence): Collect RADIUS / TACACS+ authentication server logs and MFA push notifications when identity provider integration modules are active.*

## Containment

If triage indicates probable credential compromise:

1. Immediately force password reset and terminate all active sessions for `user_id`.
2. Revoke active OAuth / API access tokens associated with the account.
3. Temporarily isolate the affected endpoint (`device`) from the internal network.

## Investigation

Analyst must explicitly determine and document:
- **False Positive / Benign Failure:** User mistyped password or forgot credentials during off-hours shift; no unauthorized access occurred.
- **Brute Force / Password Spray Attempt:** Multiple failed login attempts originating from external source, but target account remained secure (`outcome == "FAILURE"`).
- **Confirmed Account Compromise:** Adversary successfully authenticated using stolen credentials (`outcome == "SUCCESS"` after failures) and performed subsequent actions.

## Eradication / Remediation

- Force mandatory multi-factor authentication (MFA) re-enrollment for compromised account.
- Scan the affected `device` for credential harvesting malware or keyloggers.
- Audit Active Directory for unauthorized group membership changes or newly created service accounts.

## Recovery

- Restore user account access following identity verification and MFA reset.
- Monitor `user_id` authentication logs for 48 hours to confirm normal access patterns.
- Mark incident status (`RESOLVED` or `CONTAINED`) in the HAI-SOC incidents module.

## Escalation Criteria

Escalate immediately to the Incident Response Lead if:
- Compromised account holds `ADMIN` or domain-administrator privileges.
- Subsequent unauthorized PHI export (`EXPORT_PHI`) occurred under the compromised session.
- Credential stuffing activity targets multiple accounts across clinical departments simultaneously.

## HAI-SOC Detection Mapping

- **Log Action:** `LOGIN`, `API_REQUEST`
- **Telemetry Schema Fields:** `user_id`, `role`, `department`, `source`, `destination`, `device`, `outcome`, `extra.failed_attempts`, `extra.unusual_hour`
- **Anomaly Classifier:** `xgboost_v1`, `isolation_forest_v1`
- **Risk Level Assignment:** `CRITICAL` (score $\ge 0.90$) or `HIGH` (score $\ge 0.75$)

## Related Knowledge

During investigation, retrieve the following existing HAI-SOC knowledge base modules:

- **HIPAA:**
  - `knowledge_base/hipaa/technical_safeguards.md` (Authentication & Access Control: 45 CFR § 164.312(a)(1), (d))
- **NIST:**
  - `knowledge_base/nist/access_control.md` (Account Management & Privilege: AC-2, AC-6)
  - `knowledge_base/nist/identification_authentication.md` (Identification & Authentication: IA-2, IA-5)
  - `knowledge_base/nist/audit_accountability.md` (Event Logging: AU-2, AU-3)
  - `knowledge_base/nist/incident_response.md` (Incident Handling: IR-4, IR-5)
- **MITRE ATT&CK:**
  - `knowledge_base/mitre/T1078_valid_accounts.md` (Valid Accounts: T1078)
