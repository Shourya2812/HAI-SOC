# 🏥 HAI-SOC

### Healthcare AI Security Operations Platform

> An AI-powered SOC platform that replaces rule-based healthcare log monitoring with ML-driven anomaly detection, RAG-grounded compliance context, and a GenAI incident-reporting copilot.

---

## Overview

Healthcare organizations generate huge volumes of security logs across EHRs, IoT devices, cloud services, and network infrastructure — far more than analysts can manually triage. Traditional rule-based SIEMs respond with high false-positive rates and no behavioral context.

HAI-SOC ingests and normalizes multi-source healthcare security logs, scores them for anomalousness using unsupervised machine learning, and (in progress) retrieves relevant HIPAA/NIST/MITRE ATT&CK context via RAG so a GenAI copilot can generate explainable, analyst-ready incident reports — not just a raw anomaly score.

## Status

**Phase: ML anomaly detection benchmarking complete → moving into RAG + GenAI copilot**

| Area | Status |
|---|---|
| Backend API (FastAPI, MongoDB, CRUD) | ✅ Done |
| Auth, RBAC, global exceptions, audit logs | ✅ Done |
| Synthetic healthcare security dataset + 5-attack injector | ✅ Done |
| ML anomaly detection — 5 models trained & benchmarked | ✅ Done |
| Data leakage investigation & fix (`severity_score`) | ✅ Done |
| Correlated attack sequences (multi-stage) | 🚧 Planned |
| RAG knowledge layer (HIPAA/NIST/MITRE) | 🚧 Planned |
| GenAI incident copilot (LangGraph agents) | 🚧 Planned |
| React dashboard | 🚧 Planned |
| Kafka streaming ingestion | 🚧 Planned |
| Kubernetes + AWS deployment | 🚧 Planned |

## Architecture

```text
Healthcare log sources (EHR, VPN, Firewall, Network, IAM)
        │
        ▼
Ingestion & normalization (FastAPI → MongoDB)
        │
        ▼
Feature engineering (categorical encoding, time features, scaling)
        │
        ▼
ML anomaly detection (Isolation Forest / LOF / One-Class SVM / Autoencoder / XGBoost)
        │
        ▼
Prediction API  ──▶  [planned] Alert orchestrator (LangGraph)
                            │
                            ├── MITRE ATT&CK mapping
                            ├── Compliance retrieval (RAG — HIPAA/NIST)
                            ├── Historical incident search
                            └── Asset context
                            │
                            ▼
                     GenAI incident report
```

## Machine Learning — Model Benchmark

Five models were trained on an identical feature set and chronological train/test split for a fair comparison across unsupervised and supervised approaches:

| Model | Type | Precision | Recall | F1 | ROC-AUC | FPR |
|---|---|---|---|---|---|---|
| XGBoost* | Supervised | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |
| Isolation Forest | Unsupervised | 0.944 | 0.531 | 0.680 | 0.900 | 0.003 |
| AutoEncoder | Unsupervised | 0.850 | 0.531 | 0.654 | 0.866 | 0.008 |
| One-Class SVM | Unsupervised | 0.875 | 0.438 | 0.583 | 0.810 | 0.006 |
| LOF | Unsupervised | 0.192 | 0.313 | 0.238 | 0.740 | 0.117 |

*XGBoost's initial perfect score was investigated and traced to `severity_score` acting as a near-deterministic label proxy (a SIEM-assigned field, not observed behavior) — a genuine data leakage finding, since fixed in the feature engineering pipeline. See `docs/ARCHITECTURE.md` for the full write-up.

**Key finding:** Isolation Forest leads the unsupervised field, but all models struggle on `INSIDER_THREAT` — a volume/pattern-based attack with no single-event signature, which point-anomaly models structurally can't catch without session-level aggregated features. This is the direction the next iteration of the attack dataset and feature set is heading.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| Database | MongoDB |
| Vector DB | Qdrant *(planned)* |
| ML | Scikit-learn, PyOD, XGBoost |
| GenAI | LangChain + LangGraph *(planned)* |
| LLM | API-based (Anthropic) *(planned)* |
| Frontend | React + TypeScript + Tailwind *(planned)* |
| Auth | JWT + RBAC |
| Cache | Redis *(planned)* |
| Streaming | Kafka *(planned)* |
| Deployment | Docker + Kubernetes *(planned)* |
| Cloud | AWS *(planned)* |

## Project Structure

```text
HAI-SOC/
├── backend/          FastAPI app, models, CRUD, auth, RBAC, audit logs
├── frontend/          React + TypeScript dashboard (planned)
├── ml/                config, feature engineering, evaluation, utils
│   ├── models/        isolation_forest, lof, one_class_svm, autoencoder, xgboost
│   ├── training/       comparison & diagnostic scripts
│   └── artifacts/      trained models + metrics (gitignored where large)
├── datasets/
│   ├── generators/     ehr_log_generator.py, attack_injector.py
│   └── processed/      ml_dataset.csv
├── rag/                RAG ingestion, embeddings, retrieval (planned)
├── knowledge_base/     HIPAA/NIST/MITRE reference docs (planned)
├── deployment/          Docker, Kubernetes, Helm
├── monitoring/          Prometheus, Grafana
├── docs/                ARCHITECTURE.md — full design & decision log
└── tests/
```

## API

| Method | Endpoint | Description |
|---|---|---|
| POST | `/logs` | Ingest a normalized security log event |
| GET | `/logs` | List/filter logs |
| GET | `/logs/{id}` | Retrieve a single log |
| PATCH | `/logs/{id}` | Update a log |
| DELETE | `/logs/{id}` | Delete a log |
| POST | `/predict` | Run ML anomaly scoring on a log event |

Interactive docs (Swagger): `http://localhost:8000/docs`

## Getting Started

```bash
git clone https://github.com/Shourya2812/HAI-SOC.git
cd HAI-SOC

# Backend
python -m venv backend/.venv
source backend/.venv/Scripts/activate   # or backend/.venv/bin/activate on macOS/Linux
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload

# Generate the synthetic dataset
python -m datasets.generators.attack_injector

# Train and benchmark all ML models
python -m ml.training.compare_models
```

Full architecture, tech stack rationale, and decision log: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

## Roadmap

- [x] Backend API, MongoDB, CRUD
- [x] Auth, RBAC, audit logging
- [x] Synthetic dataset + attack injector
- [x] ML anomaly detection (5-model benchmark)
- [x] Data leakage investigation
- [ ] Correlated multi-stage attack sequences
- [ ] RAG knowledge layer (HIPAA/NIST/MITRE ATT&CK)
- [ ] GenAI incident copilot (LangGraph)
- [ ] React dashboard
- [ ] Kafka streaming
- [ ] Kubernetes + AWS deployment
- [ ] Monitoring (Prometheus/Grafana)
- [ ] CI/CD

## Author

**Shourya Tiwari**
Computer Science Engineering (Cybersecurity), Manipal Institute of Technology