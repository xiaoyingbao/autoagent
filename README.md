# Week 5 Status Update

## 1. Project Summary

**Project:** AutoAgent — A Multi-Agent LLM Orchestration System

**Goal:** Build a production-grade system where three specialized LLM agents (Planner, Executor, Reviewer) collaborate in a pipeline to solve complex technical decision queries. The system is deployed on GCP Cloud Run with a full CI/CD pipeline via GitHub Actions. Final demo in Week 7.

**Overall Project Timeline:**

| Week | Focus | Status |
|------|-------|--------|
| Week 1 | Project design, architecture, environment setup | ✅ Done |
| Week 2 | Planner Agent + basic Executor Agent | ✅ Done |
| Week 3 | Full Executor + Reviewer Agent + end-to-end pipeline | ✅ Done |
| Week 4 | Redis task queue + Docker + CI/CD via GitHub Actions | ✅ Done |
| Week 5 | GCP Cloud Run deployment + monitoring | ✅ Done ← Current |
| Week 6 | Streamlit UI + demo preparation | 🔲 Upcoming |
| Week 7 | Final Demo | 🔲 Upcoming |

**Recent Updates (Week 5):**
- Deployed containerized application to **GCP Cloud Run** using Docker image from GCR
- Configured **Cloud SQL (PostgreSQL)** as production database on GCP
- Set up **GCP Secret Manager** for secure API key management
- Enabled CI/CD auto-deploy to Cloud Run on every push to main
- Added **Cloud Monitoring** dashboard tracking request count, latency, and error rate
- Configured health check endpoint for Cloud Run startup probe

---

## 2. Team Members

| Name | Role |
|------|------|
| Xiaoying Bao | Solo Developer — System Architect, Backend Engineer, MLOps Engineer |

*No changes.*

---

## 3. Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                   User / Client                      │
└──────────────────────┬──────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼──────────────────────────────┐
│           GCP Cloud Run (FastAPI)          ✅ NEW    │
│         Auto-scaling · HTTPS · Managed               │
└──────────────────────┬──────────────────────────────┘
                       │ enqueue task
┌──────────────────────▼──────────────────────────────┐
│          Redis Task Queue (Celery Broker)            │
└───────┬──────────────────────────┬──────────────────┘
        │                          │
┌───────▼────────┐      ┌──────────▼─────────────────┐
│ Planner Agent  │─────▶│     Executor Agent(s)       │
└────────────────┘      └──────────┬─────────────────┘
                                   │
                        ┌──────────▼─────────────────┐
                        │      Reviewer Agent         │
                        └──────────┬─────────────────┘
                                   │
                        ┌──────────▼─────────────────┐
                        │  Cloud SQL (PostgreSQL)     │  ✅ NEW
                        │  Logs · Metrics · History   │
                        └────────────────────────────┘

CI/CD: GitHub Actions → GCR → Cloud Run auto-deploy   ✅ NEW
Monitoring: Cloud Monitoring dashboard                 ✅ NEW
```

---

## 4. Tech Stack

| Category | Technology | Status |
|----------|-----------|--------|
| Language | Python 3.11 | ✅ Set up |
| Agent Framework | LangChain | ✅ Implemented |
| LLM Backend | OpenAI API (GPT-4o-mini) | ✅ Configured |
| API Layer | FastAPI + Pydantic | ✅ Implemented |
| Agent - Planner | LangChain + OpenAI | ✅ Implemented (Week 2) |
| Agent - Executor | LangChain + OpenAI | ✅ Implemented (Week 3) |
| Agent - Reviewer | LangChain + OpenAI | ✅ Implemented (Week 3) |
| Task Queue | Redis + Celery | ✅ Async pipeline (Week 4) |
| Containerization | Docker + Docker Compose | ✅ Full stack (Week 4) |
| CI/CD | GitHub Actions | ✅ test → build → deploy (Week 5) |
| Container Registry | Google Container Registry | ✅ Image pushed (Week 5) |
| Cloud Deployment | GCP Cloud Run | ✅ Live (Week 5) |
| Database | Cloud SQL (PostgreSQL) | ✅ Production DB (Week 5) |
| Monitoring | GCP Cloud Monitoring | ✅ Dashboard set up (Week 5) |
| Frontend UI | Streamlit | 🔲 Planned (Week 6) |

---

## 5. Technical Demo

**Demo Topic:** Live Cloud Deployment — AutoAgent Running on GCP Cloud Run

**What to show:**

1. Open the live **Cloud Run URL** in the browser — show the app is running on GCP (not localhost)
2. Submit a query via the live Swagger UI (`/docs`) — demonstrate the full pipeline running in the cloud
3. Show **GCP Console → Cloud Run** — live request count, latency metrics, instance scaling
4. Show **GitHub Actions** — CI/CD auto-deployed the latest Docker image to Cloud Run

**Demo Script:**

*"This week I deployed AutoAgent to GCP Cloud Run. Unlike last week where everything ran locally, the system is now live on Google's infrastructure. I'm submitting a query directly to the Cloud Run URL — you can see the Planner, Executor, and Reviewer Agents running in the cloud, with results logged to Cloud SQL. The Cloud Monitoring dashboard shows real-time request count and latency. Every push to GitHub automatically builds a new Docker image and deploys it to Cloud Run — fully automated."*

---

## 6. Plan for Next Week (Week 6)

- Build **Streamlit UI** — input field for user query, real-time display of Planner subtasks, Executor results, and Reviewer final answer
- Connect Streamlit frontend to the live Cloud Run API endpoint
- Polish UI for final demo presentation
- Prepare **final demo script** and rehearse end-to-end walkthrough
- Update README with live deployment URL and demo instructions

---

## 7. Blockers / Risks

| Issue | Risk Level | Mitigation |
|-------|-----------|------------|
| Cloud SQL connection from Cloud Run | Medium | Use Cloud SQL Auth Proxy connector |
| OpenAI API cost in production | Low | GPT-4o-mini + $5 usage limit |
| Cloud Run cold start latency | Low | Minimum 1 instance configured to avoid cold starts |
| Redis on GCP (Memorystore cost) | Medium | Use Redis Labs free tier as alternative |
| Solo workload management | Low | On track, two weeks remaining |