---
document_id: hipaa-breach-notification-v1
category: HIPAA
framework: HIPAA
title: HIPAA Breach Notification Rule (45 CFR §§ 164.400–414)
source: HHS
citation: 45 CFR §§ 164.400–414
tags:
  - hipaa
  - breach_notification
  - security_incident
  - phi_exfiltration
  - breach_assessment
  - hhs_reporting
---

# HIPAA Breach Notification Rule (45 CFR §§ 164.400–414)

## Source

Authoritative Federal Regulation: U.S. Department of Health and Human Services (HHS), Title 45 of the Code of Federal Regulations (CFR), Part 164, Subpart D — Notification in the Case of Breach of Unsecured Protected Health Information, Sections 164.400 through 164.414.

## Requirement

A covered entity must, following the discovery of a breach of unsecured protected health information (PHI), notify each individual whose unsecured PHI has been, or is reasonably believed by the covered entity to have been, accessed, acquired, used, or disclosed as a result of such breach.

### 1. Definition of Breach & Risk Assessment — 45 CFR § 164.402
An acquisition, access, use, or disclosure of protected health information in a manner not permitted under Subpart E of Part 164 which compromises the security or privacy of the protected health information.

An acquisition, access, use, or disclosure of PHI is presumed to be a breach unless the covered entity or business associate demonstrates that there is a low probability that the PHI has been compromised based on a risk assessment of at least the following four factors:
1. The nature and extent of the PHI involved, including the types of identifiers and the likelihood of re-identification.
2. The unauthorized person who used the PHI or to whom the disclosure was made.
3. Whether the PHI was actually acquired or viewed.
4. The extent to which the risk to the PHI has been mitigated.

### 2. Notification to Individuals — 45 CFR § 164.404
- **Timing:** Written notification provided without unreasonable delay and in no case later than 60 calendar days after discovery of a breach by the covered entity or business associate.
- **Content:** Description of what occurred, types of PHI involved, steps individuals should take to protect themselves, investigation/mitigation steps taken by the entity, and contact procedures.

### 3. Notification to the Media — 45 CFR § 164.406
For a breach of unsecured PHI involving more than 500 residents of a State or jurisdiction, the covered entity must notify prominent media outlets serving the State or jurisdiction without unreasonable delay and no later than 60 calendar days after discovery.

### 4. Notification to the Secretary of HHS — 45 CFR § 164.408
- **Breaches involving 500 or more individuals:** Notice must be provided to the Secretary concurrently with notice to individuals (without unreasonable delay, within 60 days).
- **Breaches involving fewer than 500 individuals:** Notice must be submitted to the Secretary in an annual report submitted within 60 days of the end of the calendar year.

### 5. Notification by a Business Associate — 45 CFR § 164.410
A business associate must notify the covered entity without unreasonable delay and in no case later than 60 calendar days after discovery of a breach of unsecured PHI.

### 6. Administrative Requirements & Burden of Proof — 45 CFR § 164.414
The covered entity or business associate has the burden of proof to demonstrate that all notifications were provided as required or that an impermissible use or disclosure did not constitute a breach.

## HAI-SOC Relevance

> [!NOTE]
> **HAI-SOC Platform Application & Technical Interpretation**
> The following operational mapping reflects how the HAI-SOC AI Security Operations platform assists SOC analysts in assessing potential breach severity and maintaining audit evidence.

HAI-SOC provides automated telemetry analysis to accelerate breach assessment and satisfy § 164.414 burden-of-proof requirements:
- **Mass PHI Access Detection (§ 164.402 Risk Factor 1 & 3):** High-volume data transfers or queries (`action == "EXPORT_PHI"` or `action == "QUERY_DATABASE"` with `records_accessed > 100`) automatically trigger `CRITICAL` risk incidents to flag potential unauthorized PHI acquisition.
- **Unusual Egress & Exfiltration (§ 164.402 Risk Factor 2):** Outbound connections (`NETWORK_CONNECTION` with high `bytes_sent` to unapproved IP destinations) alert analysts to potential PHI exfiltration.
- **Burden of Proof & Audit Logging (§ 164.414):** HAI-SOC maintains immutable log references (`log_id`) and timestamped anomaly detection records (`created_at`, `anomaly_score`) for every security incident to document discovery timeline and technical findings.

## Security Events Relevant to HAI-SOC

- `EXPORT_PHI`: Bulk export of patient records; primary telemetry for potential breach scope determination.
- `QUERY_DATABASE`: High-count database query activity affecting patient databases.
- `FILE_ACCESS`: Access or copying of medical image archives or patient export files.
- `NETWORK_CONNECTION`: Outbound network transfers to external IP addresses.
- `LOGIN`: Compromised account usage resulting in unauthorized PHI access.
- `API_REQUEST`: Automated API data extraction attempts.

## Citation

U.S. Department of Health and Human Services (HHS), Office for Civil Rights (OCR). 45 CFR Subpart D — Notification in the Case of Breach of Unsecured Protected Health Information (§§ 164.400–164.414). Available via HHS.gov / eCFR.
