# HAI-SOC — Architecture

## 1. Problem statement (short form)

Healthcare orgs generate huge volumes of security logs (EHR access, IoT devices, cloud, auth, network) that traditional rule-based SIEMs can't triage well — too many false positives, no context, heavy manual investigation. HAI-SOC ingests and normalizes these logs, detects anomalies with unsupervised ML, retrieves relevant compliance/threat-intel context via RAG, and uses an LLM to generate analyst-ready incident reports, threat assessments, and remediation guidance — deployed as a cloud-native, containerized, HIPAA-aware platform.

## 2. Goals / non-goals

**Goals**
- End-to-end pipeline: raw log → normalized event → anomaly score → correlated incident → explainable AI-generated report
- Explainability: every AI output should cite the retrieved policy/technique it's grounded in
- Production-shaped: RBAC, audit logging, containerized, orchestrated, monitored, CI/CD'd

**Non-goals (for v1)**
- Real PHI/real hospital data — use simulated or public security-log datasets only
- Real-time streaming at scale — batch + near-real-time is enough to demonstrate the concept
- A fully custom LLM — use an existing model (API-based or Ollama) via LangChain/LangGraph, not train one

## 3. High-level architecture

```
Log sources (EHR, IoT, auth, cloud, network)
        │
        ▼
Ingestion pipeline
  Wazuh agents → Kafka → Parser → Normalizer → Cleaner → Feature engineering → MongoDB
        │
        ▼
ML anomaly detection service
  Isolation Forest / LOF / Autoencoder → anomaly_score, risk_score, confidence, severity
        │
        ▼
Alert orchestrator (LangGraph)
  routes each incident to specialist agents, runs them in parallel:
        ├── MITRE ATT&CK mapping agent
        ├── Compliance retrieval agent      (HIPAA / NIST — RAG over ChromaDB)
        ├── Historical incident search agent
        └── Asset context agent
        │
        ▼
Report generator
  synthesizes agent outputs → incident summary, threat assessment, HIPAA impact, remediation steps
        │
        ▼
Backend API (FastAPI)
  POST /logs · POST /detect · POST /ask · GET /alerts · GET /dashboard · GET /reports
        │
        ▼
Frontend dashboard (React + TypeScript + Tailwind)
  Dashboard · Alerts · Logs · Threat investigation · RAG chat · Reports · Analytics · Settings
```

Auth (JWT + RBAC), Redis (caching/session), Prometheus/Grafana (monitoring), and Kafka (message queue between ingestion and ML service) sit alongside this pipeline as cross-cutting infrastructure — see section 6.

## 4. Module breakdown

| Module | Responsibility | Key tech |
|---|---|---|
| Ingestion | Collect, parse, normalize, enrich raw logs | Wazuh, Kafka, Python |
| Storage | Persist normalized events, scores, incidents | MongoDB |
| ML detection | Score events for anomalousness | Scikit-learn, PyOD, XGBoost |
| Orchestrator | Route incidents to specialist agents, manage agent state | LangGraph |
| RAG layer | Chunk, embed, retrieve compliance/threat-intel docs | Sentence Transformers, Qdrant |
| GenAI copilot | Generate grounded incident reports | LangChain + LLM (API) |
| Backend API | Expose all functionality over REST | FastAPI |
| Frontend | SOC analyst-facing UI | React, TypeScript, Tailwind, Chart.js |
| Auth | Authentication + role-based access | JWT, FastAPI middleware |
| Infra | Containerize, orchestrate, deploy | Docker, Kubernetes, Helm, AWS |
| Monitoring | Track system health and detection throughput | Prometheus, Grafana |

## 5. Data flow narrative

1. A log event (e.g. a failed EHR login) is generated at the source and shipped by a Wazuh agent.
2. It lands in Kafka, gets picked up by the ingestion service, parsed into the common schema, cleaned, enriched, and written to MongoDB.
3. The ML service scores the event (and related events) for anomalousness, producing an anomaly score, risk score, confidence, and severity.
4. If the score crosses threshold, the alert orchestrator creates an incident and dispatches it to four agents in parallel: MITRE mapping, compliance lookup, historical search, asset context.
5. The report generator combines all four agent outputs into one incident report: what happened, root cause, MITRE technique, affected assets, risk level, HIPAA impact, and remediation steps — each claim traceable to a retrieved source.
6. The API exposes this to the frontend, where a SOC analyst (or compliance officer, or admin — per RBAC) views it on the dashboard or asks follow-up questions via the RAG chat.

## 6. Common log schema (used across all sources)

```
timestamp, source, destination, user, role, device,
department, action, severity, protocol, port, message, outcome
```

## 7. Tech stack (with one-line justification each)

| Layer | Choice | Why |
|---|---|---|
| Backend | FastAPI | Async, fast, automatic OpenAPI docs |
| ML | Scikit-learn, PyOD, XGBoost | Direct reuse of your AMPds/iBlend anomaly detection experience |
| Orchestration (AI) | LangChain + LangGraph | LangGraph gives explicit, debuggable agent state graphs — better than an implicit chain for a multi-agent SOC copilot |
| LLM | API Based | Faster development, better model quality, minimal infrastructure. |
| Embeddings | Sentence Transformers | Free, local, no API cost for embedding the knowledge base |
| Vector DB | Qdrant | Production-ready vector search with excellent LangChain integration |
| Database | MongoDB | Relational integrity for logs/incidents/users; mature, well-understood |
| Cache | Redis | Session storage, response caching |
| Message queue | Kafka | Decouples ingestion from ML scoring; realistic production pattern |
| Frontend | React + TypeScript + Tailwind | Type safety + fast iteration on dashboard UI |
| Infra | Docker, Kubernetes, Helm | Matches your existing Docker/K8s certification work |
| Cloud | AWS (EKS, RDS, S3, ECR, IAM, CloudWatch) | Industry-standard cloud-native deployment target |
| Monitoring | Prometheus + Grafana | Standard K8s-native observability stack |
| CI/CD | GitHub Actions | Free, integrates directly with GitHub repo |

## 8. Non-functional requirements

- **Explainability** — every AI-generated claim in a report must cite a retrieved source (policy clause, MITRE technique ID, or prior incident).
- **Security** — JWT auth, RBAC (Admin / SOC Analyst / Compliance Officer), audit log of every analyst action.
- **HIPAA-alignment** — no real PHI in the dataset; document how the design would satisfy HIPAA Security Rule technical safeguards if it handled real data.
- **Observability** — CPU, memory, API latency, error rate, detection throughput, and Kubernetes health must all be visible in Grafana.
- **Reproducibility** — anyone should be able to clone the repo and run `docker-compose up` to get a working local instance.

## 9. Repository structure

```
HAI-SOC/
├── backend/
│   ├── api/
│   ├── auth/
│   ├── services/
│   ├── models/
│   └── database/
├── frontend/
├── ml/
│   ├── preprocessing/
│   ├── training/
│   ├── inference/
│   └── evaluation/
├── rag/
│   ├── ingestion/
│   ├── embeddings/
│   ├── retrieval/
│   └── prompts/
├── datasets/
├── knowledge_base/
├── deployment/
│   ├── docker/
│   ├── kubernetes/
│   └── helm/
├── monitoring/
├── docs/
├── tests/
└── .github/
    └── workflows/
```

## 10. Decision log

Record every non-trivial choice here as you make it — this becomes useful interview material later.

| Date | Decision | Options considered | Chosen | Reason |
|---|---|---|---|---|
| Wk1 D1 | Orchestration framework | LangChain chains vs LangGraph | LangGraph | Explicit agent graph is easier to debug and extend with new agents later |
| Wk1 D2 | LLM backend | API-based (Claude/OpenAI-compatible) | LLMs |Faster development,better model quality | minimal infrastructure |
| Wk1 D2 | Vector DB | Qdrant vs FAISS vs pgvector | Qdrant | Simplest local dev experience, native LangChain support |
| Wk1 D3 | Message queue | Kafka vs simple queue/cron | Kafka | Realistic production pattern; decouples ingestion from scoring |

## 11. Milestone checklist (Phases 1–15)

- [ ] Phase 1 — Architecture & planning (Wk 1)
- [ ] Phase 2 — Healthcare security dataset (Wk 2)
- [ ] Phase 3 — Data engineering pipeline (Wk 3)
- [ ] Phase 4 — ML anomaly detection (Wk 4–5)
- [ ] Phase 5 — RAG knowledge base (Wk 6–7)
- [ ] Phase 6 — Generative AI SOC copilot (Wk 8–9)
- [ ] Phase 7 — Backend APIs (Wk 9–10)
- [ ] Phase 8 — Frontend dashboard (Wk 10–11)
- [ ] Phase 9 — Authentication & RBAC (Wk 11)
- [ ] Phase 10 — Dockerization (Wk 12)
- [ ] Phase 11 — Kubernetes deployment (Wk 13–14)
- [ ] Phase 12 — AWS deployment (Wk 15)
- [ ] Phase 13 — Monitoring (Wk 16)
- [ ] Phase 14 — CI/CD (Wk 17)
- [ ] Phase 15 — Documentation & research write-up (Wk 18)
