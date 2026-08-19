---
document_id: mitre-attack-t1567-v1
category: MITRE
framework: MITRE_ATTACK
title: Exfiltration Over Web Service (T1567)
source: MITRE ATT&CK
citation: MITRE ATT&CK T1567
technique_id: T1567
technique_name: Exfiltration Over Web Service
tactic: Exfiltration
tags:
  - mitre
  - attack
  - exfiltration
  - t1567
  - phi_exfiltration
  - web_service
  - cloud_storage
---

# Exfiltration Over Web Service (T1567)

## Source

Authoritative Knowledge Base: MITRE ATT&CK® Enterprise Matrix, Technique T1567 (Exfiltration Over Web Service). Official repository reference: https://attack.mitre.org/techniques/T1567/.

## Technique

- **Technique ID:** T1567
- **Technique Name:** Exfiltration Over Web Service
- **Tactic:** Exfiltration
- **Description:** Adversaries may use an existing, legitimate external web service to exfiltrate data from an enterprise network. Exfiltrating data over popular web services (such as cloud storage providers or code repositories) allows adversaries to blend exfiltration traffic with benign enterprise web usage, bypassing outbound network filtering.

### Sub-Techniques
- **T1567.001 — Exfiltration to Code Repository:** Transferring sensitive enterprise files or source code to public or external code hosting services.
- **T1567.002 — Exfiltration to Cloud Storage:** Uploading sensitive files or database exports to commercial cloud storage services (e.g. Mega, Dropbox, Google Drive, OneDrive).

## Detection / Data Sources

- **Network Traffic (Network Traffic Content / Flow):** Monitoring outbound HTTPS connection volume (`bytes_sent`), high-frequency POST requests, or unusual external destination domains.
- **Application Log (Application Log Content):** Auditing bulk record export actions, database extraction logs, and external API requests.

## HAI-SOC Relevance

> [!NOTE]
> **HAI-SOC Platform Application & Technical Interpretation**
> The following mapping describes how the HAI-SOC AI Security Operations platform identifies potential PHI data exfiltration events for SOC analyst investigation.

In healthcare security monitoring, unauthorized bulk extraction of patient health records (PHI) presents severe regulatory and privacy risks:
- **Bulk Record Export Anomalies:** Events featuring `action == "EXPORT_PHI"` with high `records_accessed` values (e.g. > 100 patient records) occurring during off-hours (`unusual_hour == True`) may warrant investigation for unauthorized data collection prior to exfiltration.
- **High Outbound Bandwidth:** Security logs with `action == "NETWORK_CONNECTION"` or `action == "API_REQUEST"` indicating unusually large `bytes_sent` payload transfers to external IP destinations (`destination`) could be consistent with active web service exfiltration.
- **Unusual Destination Gateways:** Telemetry recording network outbound traffic originating from internal healthcare systems (e.g. `source == "PACS"` or `source == "EHR"`) routed to unauthorized cloud destinations provides evidence relevant to potential data exfiltration.

## Security Events Relevant to HAI-SOC

- `EXPORT_PHI`: Primary log event for patient record export volumes and file download tracking.
- `NETWORK_CONNECTION`: Outbound network traffic flow monitoring (`bytes_sent`, destination IP/domain).
- `API_REQUEST`: External API POST/PUT request tracking.
- `QUERY_DATABASE`: SQL query execution yielding high record count payload returns.

## Investigation Considerations

Before classifying an anomaly as unauthorized exfiltration under MITRE Technique T1567, SOC analysts should examine:
1. Business context: Distinguish authorized administrative cloud backups or approved clinical research transfers from unauthorized exfiltration attempts.
2. User authorization check: Verify whether the `user_id` submitting the export request possesses active change tickets or approved data transfer authorizations.
3. Destination IP reputational check: Perform WHOIS and threat intelligence lookups on the `destination` IP address to evaluate reputation and domain ownership.

## Citation

MITRE ATT&CK®. Technique T1567: Exfiltration Over Web Service. Published by The MITRE Corporation. Available online at https://attack.mitre.org/techniques/T1567/.
