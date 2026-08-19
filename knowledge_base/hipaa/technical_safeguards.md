---
document_id: hipaa-technical-safeguards-v1
category: HIPAA
framework: HIPAA
title: HIPAA Security Rule Technical Safeguards (45 CFR § 164.312)
source: HHS
citation: 45 CFR § 164.312
tags:
  - hipaa
  - security_rule
  - technical_safeguards
  - access_control
  - audit_controls
  - integrity
  - authentication
  - transmission_security
---

# HIPAA Security Rule Technical Safeguards (45 CFR § 164.312)

## Source

Authoritative Federal Regulation: U.S. Department of Health and Human Services (HHS), Title 45 of the Code of Federal Regulations (CFR), Part 164, Subpart C — Security Standards for the Protection of Electronic Protected Health Information, Section 164.312 (Technical Safeguards).

## Requirement

A covered entity or business associate must implement technical policies and procedures for electronic information systems that maintain electronic protected health information (ePHI) to allow access only to those persons or software programs that have been granted access rights.

### 1. Access Control — 45 CFR § 164.312(a)(1)
Implement technical policies and procedures for electronic information systems that maintain ePHI to allow access only to those persons or software programs that have been granted access rights as specified in § 164.308(a)(4).

- **Unique User Identification (§ 164.312(a)(2)(i) - Required):** Assign a unique name and/or number for tracking and identifying user identity.
- **Emergency Access Procedure (§ 164.312(a)(2)(ii) - Required):** Establish (and implement as needed) procedures for obtaining necessary ePHI during an emergency.
- **Automatic Logoff (§ 164.312(a)(2)(iii) - Addressable):** Implement electronic procedures that terminate an electronic session after a predetermined time of inactivity.
- **Encryption and Decryption (§ 164.312(a)(2)(iv) - Addressable):** Implement a mechanism to encrypt and decrypt ePHI.

### 2. Audit Controls — 45 CFR § 164.312(b)
Implement hardware, software, and/or procedural mechanisms that record and examine activity in information systems that contain or use ePHI.

### 3. Integrity — 45 CFR § 164.312(c)(1)
Implement policies and procedures to protect ePHI from improper alteration or destruction.

- **Mechanism to Authenticate ePHI (§ 164.312(c)(2) - Addressable):** Implement electronic mechanisms to corroborate that ePHI has not been altered or destroyed in an unauthorized manner.

### 4. Person or Entity Authentication — 45 CFR § 164.312(d)
Implement procedures to verify that a person or entity seeking access to ePHI is the one claimed.

### 5. Transmission Security — 45 CFR § 164.312(e)(1)
Implement technical security measures to guard against unauthorized access to ePHI that is being transmitted over an electronic communications network.

- **Integrity Controls (§ 164.312(e)(2)(i) - Addressable):** Implement security measures to ensure that electronically transmitted ePHI is not improperly altered without detection until disposed of.
- **Encryption (§ 164.312(e)(2)(ii) - Addressable):** Implement a mechanism to encrypt ePHI whenever deemed appropriate.

## HAI-SOC Relevance

> [!NOTE]
> **HAI-SOC Platform Application & Technical Interpretation**
> The following operational mapping reflects how the HAI-SOC AI Security Operations platform translates the above regulatory requirements into automated event monitoring and anomaly scoring.

HAI-SOC consumes telemetry from electronic health records (EHR), picture archiving and communication systems (PACS), databases, and network gateways to detect technical safeguard anomalies:
- **Audit Control Verification (§ 164.312(b)):** HAI-SOC consumes raw security log events (e.g., `READ_PATIENT_RECORD`, `QUERY_DATABASE`, `EXPORT_PHI`) to ensure full audit traceability.
- **Access Control Anomaly Scoring (§ 164.312(a)(1)):** Out-of-hours accesses (`is_business_hours == 0`), role-permission mismatches (e.g., non-clinical staff accessing clinical records), or excessive PHI downloads trigger elevated ML anomaly scores.
- **Authentication Failure Patterns (§ 164.312(d)):** Repeated `LOGIN` failures (`outcome == "FAILURE"`) across short windows flag credential stuffing or brute force attempts targeting ePHI datastores.

## Security Events Relevant to HAI-SOC

- `LOGIN`: User authentication events, failed login attempts, MFA challenges.
- `EXPORT_PHI`: Bulk export or download of patient records from EHR/PACS.
- `QUERY_DATABASE`: SQL/NoSQL queries executed against backend patient databases.
- `FILE_ACCESS`: Direct file read/write operations on medical storage servers.
- `NETWORK_CONNECTION`: Inbound/outbound traffic across internal subnet boundaries.
- `API_REQUEST`: REST/gRPC API calls to healthcare microservices.
- `IMAGE_ACCESS`: Medical image requests (DICOM) on PACS servers.
- `DEVICE_TELEMETRY`: Medical device / IoMT authentication and communication logs.

## Citation

U.S. Department of Health and Human Services (HHS), Office for Civil Rights (OCR). 45 CFR § 164.312 — Technical Safeguards. Available via HHS.gov / eCFR.
