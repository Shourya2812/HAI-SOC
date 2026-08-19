---
document_id: nist-sp800-53-audit-accountability-v1
category: NIST
framework: NIST
title: NIST SP 800-53 Rev. 5 Audit and Accountability (AU) Controls
source: NIST
citation: NIST SP 800-53 Rev. 5 (AU-2, AU-3, AU-6, AU-12) / NIST SP 800-66 Rev. 2
tags:
  - nist
  - sp800_53
  - audit_accountability
  - au_2
  - au_3
  - au_6
  - au_12
  - event_logging
---

# NIST SP 800-53 Rev. 5 Audit and Accountability (AU) Controls

## Source

Authoritative Publication: National Institute of Standards and Technology (NIST) Special Publication 800-53, Revision 5 — *Security and Privacy Controls for Information Systems and Organizations*, Family: Audit and Accountability (AU), supplemented by NIST SP 800-66 Rev. 2 (*Implementing the Health Insurance Portability and Accountability Act (HIPAA) Security Rule*).

## Controls / Guidance

### 1. Event Logging — Control AU-2
The organization identifies the types of events that the system must log to support security monitoring, risk assessments, and investigations, and coordinates the event logging function with organization-defined entities.

- **Control Enhancements:**
  - **AU-2(3) Reviews and Updates:** Reviews and updates the types of events logged periodically to maintain comprehensive coverage across clinical, network, and identity systems.

### 2. Content of Audit Records — Control AU-3
The information system produces audit records that contain sufficient information to establish what event occurred, when the event occurred, where the event occurred, the source of the event, the outcome of the event, and the identity of any individuals or subjects associated with the event.

- **Required Record Attributes (AU-3):**
  1. Event timestamp
  2. Event source / component
  3. Subject / user identity
  4. Type of event / action
  5. Event outcome (Success / Failure)

### 3. Audit Record Review, Analysis, and Reporting — Control AU-6
The organization reviews and analyzes information system audit records for indications of unusual or suspicious activity, and reports findings to designated personnel.

- **Control Enhancements:**
  - **AU-6(1) Automated Process Integration:** Employs automated mechanisms to integrate audit record analysis with anomaly detection and incident management functions.

### 4. Audit Record Generation — Control AU-12
The information system provides audit record generation capability for the auditable events defined in AU-2 at designated system components.

## HAI-SOC Relevance

> [!NOTE]
> **HAI-SOC Platform Application & Technical Interpretation**
> The following operational mapping reflects how the HAI-SOC AI Security Operations platform enforces AU-3 event structure and automates AU-6 audit review.

HAI-SOC implements automated audit record processing directly matching NIST AU-3 and AU-6 controls:
- **Normalized Schema Compliance (AU-3):** Raw healthcare security logs are ingested and normalized into HAI-SOC's common log schema containing timestamp (`timestamp`), source (`source`), destination (`destination`), user (`user_id`), role (`role`), asset (`device`), department (`department`), action (`action`), severity (`severity`), protocol (`protocol`), port (`port`), message (`message`), outcome (`outcome`), and extra metadata (`extra`).
- **Automated Audit Review & Analysis (AU-6):** HAI-SOC's ML pipeline (`xgboost_v1`, `isolation_forest_v1`) provides continuous, automated audit review to flag statistical anomalies across 100% of generated audit logs.

## Security Events Relevant to HAI-SOC

- `LOGIN`: Authentication and session audit records (AU-2, AU-3).
- `QUERY_DATABASE`: Database access and query execution audit logs.
- `EXPORT_PHI`: Data egress audit records for patient records.
- `FILE_ACCESS`: Direct file system modification and access audit logs.
- `NETWORK_CONNECTION`: Subnet traversal and network gateway audit records.
- `DEVICE_TELEMETRY`: Medical device / IoMT system audit event logs.

## Citation

National Institute of Standards and Technology (NIST). NIST SP 800-53 Rev. 5, Controls AU-2, AU-3, AU-6, AU-12. NIST SP 800-66 Rev. 2, Section 3.4. Available via nist.gov.
