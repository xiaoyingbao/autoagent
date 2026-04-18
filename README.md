# 🤖 AutoAgent — Multi-Agent LLM Orchestration System

> A production-grade system where three specialized AI agents collaborate to deliver high-quality answers to complex technical decision queries.

**Live API:** https://autoagent-131706466702.us-west1.run.app  
**API Docs:** https://autoagent-131706466702.us-west1.run.app/docs

---

## 🎯 Why AutoAgent?

Traditional AI chatbots give one-shot, shallow answers to complex questions. In real business scenarios — choosing a database architecture, designing a system for scale, or evaluating cloud providers — a single model response is often incomplete and unreliable.

**Business Goal:**
Build a reliable, scalable AI decision-support system that delivers structured, high-quality answers to complex technical questions — with measurable quality scoring and full audit trail.

**Target Users:**
- Software engineering teams making architecture decisions
- Technical leads evaluating technology trade-offs
- Enterprises needing consistent, explainable AI-generated recommendations

**AutoAgent mimics how expert teams work:**
- A **Planner** breaks down the problem into focused subtasks
- An **Executor** analyzes each component independently
- A **Reviewer** validates, scores quality (0-1 scale), and consolidates the final answer

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           Streamlit UI (Frontend)        │
│       User submits technical query       │
└──────────────────┬──────────────────────┘
                   │ HTTPS POST /query
┌──────────────────▼──────────────────────┐
│      GCP Cloud Run (FastAPI Backend)     │
│      Auto-scaling · Managed · HTTPS      │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│         Redis Task Queue (Celery)        │
└──────┬───────────────────────┬──────────┘
       │                       │
┌──────▼───────┐    ┌──────────▼──────────┐
│ Planner Agent│───▶│   Executor Agent(s)  │
│ Decomposes   │    │ Analyzes each        │
│ query into   │    │ subtask via OpenAI   │
│ subtasks     │    └──────────┬──────────┘
└──────────────┘               │
                    ┌──────────▼──────────┐
                    │   Reviewer Agent     │
                    │ Validates · Scores   │
                    │ Consolidates output  │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Cloud SQL           │
                    │  PostgreSQL          │
                    │  Logs · Audit Trail  │
                    └─────────────────────┘

CI/CD: GitHub push → Actions → Artifact Registry → Cloud Run
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Agent Framework | LangChain + GPT-4o-mini | Multi-agent orchestration |
| API Layer | FastAPI + Pydantic | Backend REST API |
| Async Processing | Redis + Celery | Task queue, non-blocking execution |
| Database | Cloud SQL PostgreSQL | Result persistence + audit trail |
| Containerization | Docker + Docker Compose | Local + cloud consistency |
| CI/CD | GitHub Actions | Auto test → build → deploy |
| Container Registry | Google Artifact Registry | Docker image storage |
| Cloud Deployment | GCP Cloud Run | Serverless, auto-scaling hosting |
| Frontend | Streamlit | Interactive demo UI |
| Testing | pytest + httpx | Unit + integration tests |

---

## ✨ Key Features

- **Multi-Agent Pipeline** — Planner → Executor → Reviewer with structured output
- **Quality Scoring** — Reviewer scores answers 0-1, threshold at 0.7
- **Async Execution** — Redis + Celery for non-blocking task processing
- **Full CI/CD** — GitHub Actions auto-deploys on every push to main
- **Cloud-Native** — GCP Cloud Run with Cloud SQL PostgreSQL
- **Interactive UI** — Streamlit frontend with real-time pipeline visualization

---

## 🚀 Local Setup

### Prerequisites
- Python 3.11
- Docker + Docker Compose
- OpenAI API Key

### Run locally with Docker

```bash
git clone https://github.com/xiaoyingbao/autoagent.git
cd autoagent
cp .env.example .env
# Add your OPENAI_API_KEY to .env
docker-compose up --build
```

API available at: `http://localhost:8000/docs`

### Run Streamlit UI

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

UI available at: `http://localhost:8501`

---

## 🔄 CI/CD Pipeline

Every push to `main` triggers:

```
1. Test    → pytest runs all unit + integration tests
2. Build   → Docker image built + pushed to Artifact Registry
3. Deploy  → Cloud Run updated with new image automatically
```

---

## 📊 Sample Query & Response

**Input:**
```json
{
  "query": "Our startup expects 500K daily users. Should we use microservices or monolithic architecture?"
}
```

**Output:**
```json
{
  "task_id": "a1a05199-ef2c-4047-8670-4bb4e561ebd8",
  "subtasks_count": 4,
  "quality_score": 0.9,
  "passed": true,
  "duration_seconds": 40.35,
  "final_answer": "For a startup expecting 500K daily users, a microservices architecture is recommended..."
}
```

---

## 📁 Project Structure

```
autoagent/
├── agents/
│   ├── planner.py       # Decomposes query into subtasks
│   ├── executor.py      # Analyzes each subtask via OpenAI
│   └── reviewer.py      # Validates and scores final output
├── api/
│   └── routes.py        # FastAPI endpoints
├── db/
│   ├── models.py        # PostgreSQL schema
│   └── database.py      # Async DB connection
├── pipeline/
│   ├── orchestrator.py  # Coordinates full agent pipeline
│   ├── celery_app.py    # Celery configuration
│   └── tasks.py         # Async task definitions
├── tests/               # pytest unit + integration tests
├── streamlit_app.py     # Streamlit frontend UI
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/
    └── ci-cd.yml        # GitHub Actions pipeline
```

---