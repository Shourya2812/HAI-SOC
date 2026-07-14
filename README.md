# HAI-SOC — Healthcare AI Security Operations Platform

An AI-powered Security Operations Center platform purpose-built for healthcare environments. It ingests and normalizes security logs from EHRs, medical IoT devices, cloud services, authentication systems, and network infrastructure; detects anomalous activity using unsupervised machine learning; retrieves relevant cybersecurity and compliance knowledge through Retrieval-Augmented Generation; and uses a multi-agent LLM copilot to generate explainable, analyst-ready incident reports, threat assessments, and remediation guidance.

Traditional SIEM tools lean on rule-based detection — high false-positive rates, no contextual understanding, and heavy manual investigation. HAI-SOC replaces that with ML-driven anomaly scoring plus a grounded GenAI layer that explains *why* an event matters, maps it to MITRE ATT&CK, assesses HIPAA impact, and drafts a remediation-ready report — not just a raw alert.

**Status:** Phase 1 — Architecture & Planning

---

## What it does

1. **Ingests** logs from EHR access, IoT telemetry, VPN/auth, and cloud audit sources into a common schema
2. **Detects** anomalies with Isolation Forest, Local Outlier Factor, and Autoencoder models
3. **Orchestrates** each flagged incident through a LangGraph agent graph that runs in parallel:
   - MITRE ATT&CK technique mapping
   - HIPAA/NIST compliance retrieval (RAG over a curated knowledge base)
   - Historical incident search
   - Asset context lookup
4. **Generates** a synthesized incident report — root cause, affected assets, risk level, HIPAA impact, and containment/remediation steps — with every claim traceable to a retrieved source
5. **Serves** it all through a role-based dashboard for SOC analysts, compliance officers, and admins

## Architecture

```
Log sources (EHR, IoT, auth, cloud, network)
        │
        ▼
Ingestion pipeline (Wazuh → Kafka → parse/normalize/clean/feature-engineer → PostgreSQL)
        │
        ▼
ML anomaly detection (Isolation Forest / LOF / Autoencoder → score, risk, confidence, severity)
        │
        ▼
Alert orchestrator (LangGraph) ── fans out to ──┬── MITRE ATT&CK mapping
                                                  ├── Compliance retrieval (RAG / ChromaDB)
                                                  ├── Historical incident search
                                                  └── Asset context
        │
        ▼
Report generator (synthesizes agent outputs into one grounded incident report)
        │
        ▼
Backend API (FastAPI) → Frontend dashboard (React + TypeScript + Tailwind)
```

Full detail — module responsibilities, data flow narrative, non-functional requirements, and decision log — lives in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Tech stack

| Layer | Tech |
|---|---|
| Backend | Python, FastAPI |
| ML | Scikit-learn, PyOD, XGBoost |
| GenAI orchestration | LangChain, LangGraph |
| Embeddings / Vector DB | Sentence Transformers, ChromaDB |
| Database | MongoDB |
| Cache | Redis |
| Message queue | Apache Kafka |
| Frontend | React, TypeScript, Tailwind CSS, Chart.js |
| Infra | Docker, Kubernetes, Helm |
| Cloud | AWS (EKS, RDS, S3, ECR, IAM, CloudWatch) |
| Monitoring | Prometheus, Grafana |
| CI/CD | GitHub Actions |

## Repository structure

```
HAI-SOC/
├── backend/            # FastAPI app: api/, auth/, services/, models/, database/
├── frontend/            # React + TypeScript dashboard
├── ml/                  # preprocessing/, training/, inference/, evaluation/
├── rag/                 # ingestion/, embeddings/, retrieval/, prompts/
├── datasets/            # normalized/simulated healthcare security logs
├── knowledge_base/      # HIPAA, NIST, MITRE ATT&CK, runbooks (source docs for RAG)
├── deployment/          # docker/, kubernetes/, helm/
├── monitoring/          # Prometheus + Grafana configs
├── docs/                # ARCHITECTURE.md and other write-ups
├── tests/
└── .github/workflows/   # CI/CD pipelines
```

## Roadmap

- [ ] **Phase 1** — Architecture & planning
- [ ] **Phase 2** — Healthcare security dataset
- [ ] **Phase 3** — Data engineering pipeline
- [ ] **Phase 4** — ML anomaly detection
- [ ] **Phase 5** — RAG knowledge base
- [ ] **Phase 6** — Generative AI SOC copilot
- [ ] **Phase 7** — Backend APIs
- [ ] **Phase 8** — Frontend dashboard
- [ ] **Phase 9** — Authentication & RBAC
- [ ] **Phase 10** — Dockerization
- [ ] **Phase 11** — Kubernetes deployment
- [ ] **Phase 12** — AWS deployment
- [ ] **Phase 13** — Monitoring
- [ ] **Phase 14** — CI/CD
- [ ] **Phase 15** — Documentation & research write-up

## Getting started

> Local dev setup will be filled in once Phase 10 (Dockerization) lands — target is a single `docker-compose up` bringing up the backend, frontend, MongoDB, Redis, Kafka, and ChromaDB.

## Data & compliance note

This project uses simulated or public security-log datasets only — no real PHI is collected, stored, or processed at any stage.


