---
document_id: runbook-ransomware-v1
category: RUNBOOK
framework: INTERNAL_RUNBOOK
title: Healthcare Ransomware Response Runbook
source: HAI-SOC
citation: HAI-SOC Internal Runbook
trigger_event: FILE_ACCESS
severity_level: CRITICAL
affected_assets:
  - EHR
  - PACS
  - Patient_DB
  - IoMT
tags:
  - runbook
  - ransomware
  - data_encryption
  - impact
  - clinical_availability
  - mitre_t1486
---

# Healthcare Ransomware Response Runbook

## Purpose

This operational runbook provides a high-priority incident response sequence for SOC analysts investigating potential ransomware, bulk file encryption, or data availability disruption across clinical healthcare systems within the HAI-SOC platform.

## Trigger Conditions

An investigation under this runbook is triggered when the ML anomaly pipeline (`xgboost_v1`, `isolation_forest_v1`) flags a system event with `severity == "CRITICAL"` or `severity == "HIGH"`, crossing anomaly threshold ($\ge 0.50$), featuring one or more of the following HAI-SOC log schema indicators:

- **Primary Actions:** `action == "FILE_ACCESS"`, `action == "IMAGE_ACCESS"`, `action == "DEVICE_TELEMETRY"`, or `action == "NETWORK_CONNECTION"`
- **Target Systems:** Critical healthcare datastores or assets (`source == "PACS"`, `source == "EHR"`, `source == "Database"`, `source == "IoMT"`).
- **System Failure Indicators:** `outcome == "FAILURE"` accompanied by high-frequency file reads/writes or connection drops across clinical subnets.

> [!CAUTION]
> **Important Distinction:** A single `FILE_ACCESS` or `IMAGE_ACCESS` log anomaly does **NOT** alone confirm ransomware activity. Analysts must verify secondary forensic evidence before issuing a ransomware declaration.

## Initial Triage

SOC analysts must execute the following 8-step initial response sequence:

1. **Identify Affected Systems:** Determine which servers (`source`, `destination`, `device`) generated the initial critical alerts.
2. **Determine Scope:** Identify whether the anomaly is isolated to a single workstation or spreading across clinical departments (`department`).
3. **Isolate Affected Systems:** Disconnect affected endpoints (`device`) from the internal network immediately to prevent lateral propagation.
4. **Preserve Forensic Evidence:** Capture system memory, active process trees, and unencrypted log files before powering down hardware.
5. **Protect Critical Clinical Operations:** Verify whether clinical care systems (EHR, PACS imaging, telemetry) remain operational; transition to paper contingency procedures if required.
6. **Identify Potential Lateral Movement:** Inspect `NETWORK_CONNECTION` events originating from the affected host to identify target subnets.
7. **Assess Data Availability & Integrity:** Verify database connection states (`Patient_DB`, PACS DICOM archives) for file corruption or unhandled write locks.
8. **Coordinate Response & Recovery:** Activate the Healthcare Incident Command Structure (HICS) and inform clinical leadership.

## Evidence Collection

- Export all `FILE_ACCESS`, `IMAGE_ACCESS`, and `NETWORK_CONNECTION` log records (`log_id`) associated with the target system.
- Extract ML prediction records (`anomaly_score`, `detector`) from `anomaly_scores`.
- Preserve workstation OS event logs and network flow summaries.
- *(Future Evidence): Collect master boot record (MBR) snapshots, volume shadow copy status, and ransom note text files when endpoint agent integration modules are deployed.*

## Containment

1. Isolate infected host systems (`device`) from network switches and VLANs.
2. Disable compromised user accounts (`user_id`) across Active Directory to stop active SMB/RDP session propagation.
3. Block external command-and-control (C2) IP addresses (`destination`) at perimeter firewalls.

## Investigation

Analyst must explicitly verify secondary evidence before confirming ransomware:
- **Secondary Evidence Required:**
  1. High-rate file modification featuring non-standard file extension changes.
  2. Execution of volume shadow copy deletion commands (`vssadmin.exe delete shadows`).
  3. Creation of extortion note text or HTML files across shared drives.
- If secondary evidence is absent, classify as a non-ransomware file access anomaly or system storage fault.

## Eradication / Remediation

- Re-image infected host systems (`device`) from verified, clean golden images.
- Scan shared network drives for residual ransomware scripts or executable payloads.
- Verify active Directory domain controller health and revoke compromised credentials.

## Recovery

- Restore data volumes from offline, immutable backup repositories (PACS/EHR backups).
- Perform data integrity checks on restored patient records prior to reconnecting clinical systems.
- Resume clinical operation monitoring and update incident status (`RESOLVED` or `CONTAINED`) in the HAI-SOC incidents module.

## Escalation Criteria

Escalate immediately to Executive Leadership, Legal Counsel, and CISO if:
- Primary clinical EHR or PACS databases are rendered inaccessible.
- Ransomware encrypted files containing patient health data (potential ePHI destruction).
- Patient care operations or medical device (IoMT) functionalities are directly impacted.

## HAI-SOC Detection Mapping

- **Log Action:** `FILE_ACCESS`, `IMAGE_ACCESS`, `DEVICE_TELEMETRY`, `NETWORK_CONNECTION`
- **Telemetry Schema Fields:** `user_id`, `role`, `department`, `source`, `destination`, `device`, `severity`, `outcome`
- **Anomaly Classifier:** `xgboost_v1`, `isolation_forest_v1`
- **Risk Level Assignment:** `CRITICAL` (score $\ge 0.90$)

## Related Knowledge

During investigation, retrieve the following existing HAI-SOC knowledge base modules:

- **HIPAA:**
  - `knowledge_base/hipaa/technical_safeguards.md` (Integrity & Transmission Security: 45 CFR § 164.312(c), (e))
  - `knowledge_base/hipaa/administrative_safeguards.md` (Contingency Planning & Security Incident Procedures: 45 CFR § 164.308(a)(6), (7))
- **NIST:**
  - `knowledge_base/nist/audit_accountability.md` (Audit Record Review: AU-6)
  - `knowledge_base/nist/incident_response.md` (Incident Handling & Monitoring: IR-4, IR-5)
- **MITRE ATT&CK:**
  - `knowledge_base/mitre/T1486_data_encrypted_for_impact.md` (Data Encrypted for Impact: T1486)
