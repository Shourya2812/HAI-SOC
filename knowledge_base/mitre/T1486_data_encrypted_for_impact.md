---
document_id: mitre-attack-t1486-v1
category: MITRE
framework: MITRE_ATTACK
title: Data Encrypted for Impact (T1486)
source: MITRE ATT&CK
citation: MITRE ATT&CK T1486
technique_id: T1486
technique_name: Data Encrypted for Impact
tactic: Impact
tags:
  - mitre
  - attack
  - impact
  - t1486
  - ransomware
  - encryption
  - health_systems
---

# Data Encrypted for Impact (T1486)

## Source

Authoritative Knowledge Base: MITRE ATT&CK® Enterprise Matrix, Technique T1486 (Data Encrypted for Impact). Official repository reference: https://attack.mitre.org/techniques/T1486/.

## Technique

- **Technique ID:** T1486
- **Technique Name:** Data Encrypted for Impact
- **Tactic:** Impact
- **Description:** Adversaries may encrypt data on target systems to interrupt availability of system and network resources. Encrypting data to disrupt availability is a common ransomware tactic designed to render systems unusable or force targets into paying extortion demands to regain access to critical operational data.

## Detection / Data Sources

- **File (File Modification / Creation / Deletion):** Monitoring for rapid, high-volume file modification or creation events featuring unusual file extension appended to encrypted files.
- **Process (Process Execution):** Tracking process execution for known ransomware binaries, shadow copy deletion commands (e.g. `vssadmin.exe delete shadows`), or unauthorized encryption utilities.
- **Drive (Drive Access):** Auditing raw disk or mass storage access requests targeting medical imaging (DICOM) or database storage volumes.

## HAI-SOC Relevance

> [!NOTE]
> **HAI-SOC Platform Application & Technical Interpretation**
> The following mapping describes how the HAI-SOC AI Security Operations platform alerts analysts to potential ransomware and data destruction activity.

In healthcare environments, ransomware activity targeting electronic health record (EHR) databases or picture archiving and communication systems (PACS) presents severe clinical operational risk:
- **Rapid Mass File Modification:** High-frequency `FILE_ACCESS` or `IMAGE_ACCESS` events with `severity == "CRITICAL"` or `severity == "HIGH"` could be consistent with active ransomware file encryption routines.
- **Database Interruption Activity:** Abrupt database query failures or bulk file lock errors (`action == "QUERY_DATABASE"` with `outcome == "FAILURE"`) may warrant investigation for ransomware payload execution against patient record repositories.
- **IoMT System Disruption:** Anomalous communication loss or sudden device state changes (`action == "DEVICE_TELEMETRY"`) across clinical IoMT devices could provide evidence relevant to unauthorized encryption or disruption of medical systems.

## Security Events Relevant to HAI-SOC

- `FILE_ACCESS`: Primary telemetry for rapid file modifications, reads, and writes on file servers.
- `IMAGE_ACCESS`: Access and modification events targeting DICOM archives on PACS servers.
- `QUERY_DATABASE`: Database connection drops or unhandled storage write errors.
- `DEVICE_TELEMETRY`: Medical device connection disruptions or unexpected firmware state locks.

## Investigation Considerations

Before confirming MITRE Technique T1486 during an active healthcare security incident, SOC analysts should examine:
1. Process execution logs on the affected host to verify whether unauthorized encryption processes or shadow copy deletion commands were executed.
2. Ransom note indicators: Check for newly created text or HTML files containing extortion instructions across shared directories.
3. System backup integrity: Ensure offline or immutable backup repositories (PACS/EHR backups) remain isolated and operational.

## Citation

MITRE ATT&CK®. Technique T1486: Data Encrypted for Impact. Published by The MITRE Corporation. Available online at https://attack.mitre.org/techniques/T1486/.
