---
document_id: mitre-attack-t1078-v1
category: MITRE
framework: MITRE_ATTACK
title: Valid Accounts (T1078)
source: MITRE ATT&CK
citation: MITRE ATT&CK T1078
technique_id: T1078
technique_name: Valid Accounts
tactic: Defense Evasion, Persistence, Privilege Escalation, Initial Access
tags:
  - mitre
  - attack
  - defense_evasion
  - persistence
  - privilege_escalation
  - initial_access
  - t1078
  - valid_accounts
---

# Valid Accounts (T1078)

## Source

Authoritative Knowledge Base: MITRE ATT&CK® Enterprise Matrix, Technique T1078 (Valid Accounts). Official repository reference: https://attack.mitre.org/techniques/T1078/.

## Technique

- **Technique ID:** T1078
- **Technique Name:** Valid Accounts
- **Tactics:** Defense Evasion, Persistence, Privilege Escalation, Initial Access
- **Description:** Adversaries may obtain and abuse credentials of existing legitimate utility, domain, or service accounts. Access gained via valid accounts allows adversaries to blend in with normal administrative or user traffic, bypassing traditional perimeter defenses and security controls.

### Sub-Techniques
- **T1078.001 — Default Accounts:** Abuse of built-in or factory default credentials on hardware, appliances, or software.
- **T1078.002 — Domain Accounts:** Abuse of Active Directory / domain-managed credentials to access domain resources.
- **T1078.003 — Local Accounts:** Abuse of local operating system accounts configured on individual endpoints or workstations.
- **T1078.004 — Cloud Accounts:** Abuse of identity provider (IdP) or cloud service credentials to access SaaS/PaaS/IaaS resources.

## Detection / Data Sources

- **User Account (User Account Authentication):** Monitoring logon activity for anomalous source IPs, off-hours access, or rapid location jumps.
- **Logon Session (Logon Record):** Auditing active session duration, concurrent logins across multiple workstations, and privilege level usage.
- **Application Log (Application Log Content):** Reviewing application-level authentication logs (e.g. EHR, PACS, VPN access logs).

## HAI-SOC Relevance

> [!NOTE]
> **HAI-SOC Platform Application & Technical Interpretation**
> The following mapping describes how the HAI-SOC AI Security Operations platform flags suspicious account activity for analyst review. Log anomalies do not automatically confirm adversary compromise.

In the HAI-SOC platform, telemetry matching valid account misuse may warrant investigation for credential compromise or insider threats:
- **Off-Hours / Anomaly Cluster Access:** Security logs with `action == "LOGIN"` or `action == "API_REQUEST"` occurring during off-hours (`is_business_hours == 0` or `unusual_hour == True`) could be consistent with unauthorized account usage.
- **Failed Login Bursts Following Success:** Bursts of authentication failures (`failed_attempts > 0`) followed by a successful login could provide evidence relevant to credential guessing or password spraying prior to account compromise.
- **Role/Department Mismatch:** A clinical user account (`role == "DOCTOR"`) attempting direct administrative queries against raw database infrastructure (`source == "Database"`) may indicate stolen credential abuse.

## Security Events Relevant to HAI-SOC

- `LOGIN`: Primary telemetry for user authentication attempts, failed logon spikes, and session start events.
- `API_REQUEST`: Service and API authentication requests using access tokens or service accounts.
- `QUERY_DATABASE`: Database session authentication and privileged SQL query execution.
- `FILE_ACCESS`: Workstation file access events initiated under compromised account contexts.

## Investigation Considerations

Before assigning MITRE Technique T1078 to an active incident, SOC analysts should examine:
1. Historical baseline activity for the specific `user_id` to determine whether off-hours or remote logins are routine for their shift schedule.
2. Multi-factor authentication (MFA) logs to verify whether MFA was successfully completed during the session.
3. Concurrent session checks: Verify whether the same `user_id` was active on multiple physical endpoints or IP addresses simultaneously.

## Citation

MITRE ATT&CK®. Technique T1078: Valid Accounts. Published by The MITRE Corporation. Available online at https://attack.mitre.org/techniques/T1078/.
