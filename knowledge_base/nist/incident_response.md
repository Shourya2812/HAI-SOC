---
document_id: nist-sp800-53-incident-response-v1
category: NIST
framework: NIST
title: NIST SP 800-53 Rev. 5 Incident Response (IR) Controls & NIST SP 800-66 Rev. 2
source: NIST
citation: NIST SP 800-53 Rev. 5 (IR-4, IR-5, IR-6) / NIST SP 800-66 Rev. 2
tags:
  - nist
  - sp800_53
  - incident_response
  - ir_4
  - ir_5
  - ir_6
  - healthcare_incident_handling
---

# NIST SP 800-53 Rev. 5 Incident Response (IR) Controls & NIST SP 800-66 Rev. 2

## Source

Authoritative Publication: National Institute of Standards and Technology (NIST) Special Publication 800-53, Revision 5 — *Security and Privacy Controls for Information Systems and Organizations*, Family: Incident Response (IR), supplemented by NIST SP 800-66 Rev. 2 (*Implementing the Health Insurance Portability and Accountability Act (HIPAA) Security Rule*).

## Controls / Guidance

### 1. Incident Handling — Control IR-4
The organization implements an incident handling capability for security incidents that includes preparation, detection and analysis, containment, eradication, and recovery.

- **Control Enhancements:**
  - **IR-4(1) Automated Incident Handling Processes:** Employs automated mechanisms to support the incident handling process.

### 2. Incident Monitoring — Control IR-5
The organization tracks and documents security incidents.

- **Control Enhancements:**
  - **IR-5(1) Automated Tracking and Data Analysis:** Employs automated mechanisms to track security incidents and analyze incident data.

### 3. Incident Reporting — Control IR-6
The organization requires personnel to report suspected security incidents to the organizational incident response capability within organization-defined time periods.

- **Control Enhancements:**
  - **IR-6(1) Automated Reporting Support:** Employs automated mechanisms to assist in the reporting of security incidents to designated authorities and security leadership.

### 4. Healthcare Incident Response Guidance — NIST SP 800-66 Rev. 2
NIST SP 800-66 Rev. 2 Section 3.4 outlines incident handling requirements specifically tailored to healthcare organizations handling ePHI:
- **Detection & Triage:** Rapid identification of anomalous behavior across EHR, PACS, and clinical subnets before unauthorized ePHI exfiltration occurs.
- **Incident Escalation:** Categorizing incidents based on severity (Critical, High, Medium, Low) to prioritize SOC analyst response.

## HAI-SOC Relevance

> [!NOTE]
> **HAI-SOC Platform Application & Technical Interpretation**
> The following operational mapping reflects how the HAI-SOC AI Security Operations platform operationalizes NIST IR controls into automated incident generation and triage.

HAI-SOC implements automated incident management directly aligning with NIST IR-4, IR-5, and IR-6:
- **Automated Incident Creation (IR-4, IR-5):** When an ML model (`xgboost_v1`, `isolation_forest_v1`) predicts an anomaly (`is_anomaly == True`), `IncidentService.create_from_prediction()` automatically creates a structured Incident record in MongoDB.
- **Risk Classification & Escalation (IR-4):** HAI-SOC automatically assigns risk levels based on anomaly scores:
  - `score >= 0.90` $\rightarrow$ `CRITICAL`
  - `score >= 0.75` $\rightarrow$ `HIGH`
  - `score >= 0.50` $\rightarrow$ `MEDIUM`
  - `score < 0.50` $\rightarrow$ `LOW`
- **Incident Tracking & Reporting (IR-5, IR-6):** Incident lifecycle states (`OPEN`, `INVESTIGATING`, `CONTAINED`, `RESOLVED`, `CLOSED`) are tracked on the HAI-SOC Incident Dashboard.

## Security Events Relevant to HAI-SOC

- `EXPORT_PHI`: Bulk exfiltration events triggering high-severity incident generation.
- `LOGIN`: Account compromise events triggering credential misuse incidents.
- `QUERY_DATABASE`: Excessive or unauthorized database query incidents.
- `FILE_ACCESS`: Unauthorized access or ransomware file encryption events.
- `NETWORK_CONNECTION`: Lateral movement or C2 network traffic incidents.

## Citation

National Institute of Standards and Technology (NIST). NIST SP 800-53 Rev. 5, Controls IR-4, IR-5, IR-6. NIST SP 800-66 Rev. 2, Section 3.4. Available via nist.gov.
