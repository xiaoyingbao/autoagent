# Week 4 Status Update

## 1. Project Summary

**Project:** AutoAgent — A Multi-Agent LLM Orchestration System

**Goal:** Build a production-grade system where three specialized LLM agents (Planner, Executor, Reviewer) collaborate in a pipeline to solve complex technical decision queries. The system will be deployed on GCP Cloud Run with a full CI/CD pipeline via GitHub Actions. Final demo in Week 7.

**Overall Project Timeline:**

| Week | Focus | Status |
|------|-------|--------|
| Week 1 | Project design, architecture, environment setup | ✅ Done |
| Week 2 | Planner Agent + basic Executor Agent | ✅ Done |
| Week 3 | Full Executor + Reviewer Agent + end-to-end pipeline | ✅ Done |
| Week 4 | Redis task queue + Docker + CI/CD via GitHub Actions | ✅ Done ← Current |
| Week 5 | GCP Cloud Run deployment + monitoring | 🔲 Upcoming |
| Week 6 | Streamlit UI + demo preparation | 🔲 Upcoming |
| Week 7 | Final Demo | 🔲 Upcoming |

**Recent Updates (Week 4):**
- Integrated Redis as async task queue using Celery for non-blocking agent execution
- Dockerized the full application (FastAPI + PostgreSQL + Redis + Celery Worker via Docker Compose)
- Set up GitHub Actions CI/CD pipeline: lint → test → build Docker image → push to GCR
- Added structured logging with latency metrics per pipeline run
- Pushed Docker image to Google Container Registry (GCR) as preparation for Week 5 deployment
- Updated `requirements.txt` with Celery and Redis dependencies

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
                       │ HTTP Request
┌──────────────────────▼──────────────────────────────┐
│              API Gateway (FastAPI)                   │
│          Rate Limiting · Auth · Validation           │
└──────────────────────┬──────────────────────────────┘
                       │ enqueue task
┌──────────────────────▼──────────────────────────────┐
│          Redis Task Queue (Celery Broker)  ✅ NEW    │
└───────┬──────────────────────────┬──────────────────┘
        │ Celery Worker picks up   │
┌───────▼────────┐      ┌──────────▼─────────────────┐
│ Planner Agent  │─────▶│     Executor Agent(s)       │  ✅ Week 2-3
└────────────────┘      └──────────┬─────────────────┘
                                   │
                        ┌──────────▼─────────────────┐
                        │      Reviewer Agent         │  ✅ Week 3
                        └──────────┬─────────────────┘
                                   │
                        ┌──────────▼─────────────────┐
                        │   PostgreSQL · Redis Cache  │
                        │   Logs · Latency · History  │  ✅ Week 3-4
                        └────────────────────────────┘

Docker Compose Services:  api | redis | db | celery_worker  ✅ NEW
GitHub Actions:           lint → test → build → push GCR     ✅ NEW
```

---

## 4. Tech Stack

| Category | Technology | Status |
|----------|-----------|--------|
| Language | Python 3.11 | ✅ Set up |
| Agent Framework | LangChain | ✅ Installed & tested |
| LLM Backend | OpenAI API (GPT-4o-mini) | ✅ Configured |
| API Layer | FastAPI + Pydantic | ✅ Implemented |
| Agent - Planner | LangChain + OpenAI | ✅ Implemented (Week 2) |
| Agent - Executor | LangChain + OpenAI | ✅ Full implementation (Week 3) |
| Agent - Reviewer | LangChain + OpenAI | ✅ Implemented (Week 3) |
| Database | PostgreSQL | ✅ Schema + logging (Week 3) |
| Task Queue | Redis + Celery | ✅ Async pipeline (Week 4) |
| Containerization | Docker + Docker Compose | ✅ Full stack (Week 4) |
| CI/CD | GitHub Actions | ✅ test → build → GCR push (Week 4) |
| Container Registry | Google Container Registry | ✅ Image pushed (Week 4) |
| Cloud Deployment | GCP Cloud Run | 🔲 Planned (Week 5) |
| Frontend UI | Streamlit | 🔲 Planned (Week 6) |

---

## 5. Technical Demo

*(Demo every other week — Week 4 is a demo week)*

**Demo Topic:** Async Pipeline Execution + Docker + CI/CD Live Walkthrough

**What to show:**

1. Show `docker-compose up` spinning up all 4 services (api, redis, db, celery_worker) — demonstrate the fully containerized stack running locally
2. Submit a query via `/query` API — show the task being enqueued to Redis and picked up asynchronously by the Celery worker
3. Show structured logs with per-agent latency metrics (Planner / Executor / Reviewer timing)
4. Show GitHub Actions workflow passing: lint → test → Docker build → push to GCR

**Demo Script:**

*"This week I completed the infrastructure layer. I'm running the entire system — FastAPI, Redis, PostgreSQL, and a Celery worker — with a single `docker-compose up`. When I submit a query, the API immediately returns a task ID while the Celery worker processes the pipeline asynchronously. You can see the structured logs showing each agent's latency. I also set up GitHub Actions — every push to main automatically runs tests, builds a Docker image, and pushes it to Google Container Registry. Next week, that image gets deployed to GCP Cloud Run."*

---

## 6. Plan for Next Week (Week 5)

- Deploy containerized application to **GCP Cloud Run** using the GCR image built by CI/CD
- Set up **Cloud SQL (PostgreSQL)** on GCP to replace local database
- Configure **Redis on GCP** (Cloud Memorystore or Redis Labs free tier)
- Add **health check endpoint** and Cloud Run startup probe
- Set up basic **Cloud Monitoring** dashboard (request count, latency, error rate)
- Update CI/CD to auto-deploy to Cloud Run on successful build

---

## 7. Blockers / Risks

| Issue | Risk Level | Mitigation |
|-------|-----------|------------|
| OpenAI API cost | Low | GPT-4o-mini, $5 usage limit set |
| GCP Cloud SQL connection from Cloud Run | Medium | Use Cloud SQL Auth Proxy; document in README |
| Celery worker cold start latency | Low | Pre-warm via `/health` endpoint |
| GitHub Actions GCP auth setup | Medium | Using Service Account JSON key stored in GitHub Secrets |
| Solo workload management | Medium | Strict weekly milestones, scope limited to core features |

