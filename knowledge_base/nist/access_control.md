---
document_id: nist-sp800-53-access-control-v1
category: NIST
framework: NIST
title: NIST SP 800-53 Rev. 5 Access Control (AC) Controls
source: NIST
citation: NIST SP 800-53 Rev. 5 (AC-2, AC-3, AC-6) / NIST SP 800-66 Rev. 2
tags:
  - nist
  - sp800_53
  - access_control
  - ac_2
  - ac_3
  - ac_6
  - least_privilege
---

# NIST SP 800-53 Rev. 5 Access Control (AC) Controls

## Source

Authoritative Publication: National Institute of Standards and Technology (NIST) Special Publication 800-53, Revision 5 — *Security and Privacy Controls for Information Systems and Organizations*, Family: Access Control (AC), supplemented by NIST SP 800-66 Rev. 2 (*Implementing the Health Insurance Portability and Accountability Act (HIPAA) Security Rule*).

## Controls / Guidance

### 1. Account Management — Control AC-2
The organization manages information system accounts, including establishing, activating, modifying, reviewing, disabling, and removing accounts in accordance with organizational procedures and guidance.

- **Control Enhancements:**
  - **AC-2(1) Automated System Account Management:** Employs automated mechanisms to support the management of information system accounts.
  - **AC-2(3) Disable Inactive Accounts:** Automatically disables inactive accounts after an organization-defined time period.
  - **AC-2(7) Role-Based Schemes:** Establishes and administers privileged and non-privileged accounts in accordance with role-based access control (RBAC) schemes.

### 2. Access Enforcement — Control AC-3
The information system enforces approved authorizations for logical access to information and system resources in accordance with applicable access control policies.

- **NIST SP 800-66 Rev. 2 Alignment:** Direct mapping to HIPAA Technical Safeguards under 45 CFR § 164.312(a)(1) (Access Control), requiring technical access rules enforcing role-based permissions on electronic health records (EHR) and clinical databases.

### 3. Least Privilege — Control AC-6
The organization employs the principle of least privilege, allowing only authorized accesses for users (or processes acting on behalf of users) which are necessary to accomplish assigned tasks in accordance with organizational missions and business functions.

- **Control Enhancements:**
  - **AC-6(1) Authorize Access to Security Functions:** Authorizes access to administrative and security functions only for explicitly designated roles.
  - **AC-6(7) Review of Role Privileges:** Reviews system privileges periodically to maintain least privilege enforcement.

## HAI-SOC Relevance

> [!NOTE]
> **HAI-SOC Platform Application & Technical Interpretation**
> The following operational mapping reflects how the HAI-SOC AI Security Operations platform utilizes NIST AC controls to detect role-permission violations and anomalous access patterns.

HAI-SOC operationalizes NIST AC controls through automated telemetry feature extraction:
- **Least Privilege & Role-Based Drift (AC-3, AC-6):** FeatureBuilder extracts log attributes `role` (e.g. `DOCTOR`, `SOC_ANALYST`, `NURSE`, `ADMIN`) and `department` (e.g. `IT`, `PHARMACY`, `RADIOLOGY`). The ML pipeline flags anomalous attempts by non-privileged accounts accessing sensitive datastores or security management systems (`action == "EXPORT_PHI"` or `action == "QUERY_DATABASE"`).
- **Inactive / Out-of-Hours Account Usage (AC-2):** Out-of-hours user activities (`is_business_hours == 0` or `unusual_hour == True`) trigger elevated anomaly scores for account misuse monitoring.

## Security Events Relevant to HAI-SOC

- `LOGIN`: Account activation and authentication monitoring.
- `EXPORT_PHI`: Data access enforcement checks under AC-3 and AC-6.
- `QUERY_DATABASE`: Database queries evaluated for role-based privilege boundaries.
- `FILE_ACCESS`: Direct file access events evaluated against AC-6 least privilege policies.
- `API_REQUEST`: Service-to-service calls evaluated for authorization tokens and role scope.

## Citation

National Institute of Standards and Technology (NIST). NIST SP 800-53 Rev. 5, Controls AC-2, AC-3, AC-6. NIST SP 800-66 Rev. 2, Section 3.4. Available via nist.gov.
