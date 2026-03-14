# AutoAgent — Multi-Agent LLM Orchestration System

A production-grade multi-agent system where three specialized LLM agents 
(Planner → Executor → Reviewer) collaborate in a pipeline to solve complex 
technical decision queries.

**Course:** LLMOps @ Northeastern University  
**Student:** Xiaoying Bao  
**Current Status:** Week 3 — Full pipeline complete (Planner → Executor → Reviewer)

---

## Architecture

```
User Request
    ↓
[FastAPI Gateway]
    ↓
[Planner Agent]  → decomposes query into 3–5 subtasks
    ↓
[Executor Agent(s)]  → analyzes each subtask independently via OpenAI
    ↓
[Reviewer Agent]  → validates, consolidates, scores quality (0.0–1.0)
    ↓
Final Response + logged to SQLite/PostgreSQL
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| Agent Framework | LangChain |
| LLM Backend | OpenAI GPT-4o-mini |
| API | FastAPI + Pydantic |
| Database | PostgreSQL (SQLAlchemy async) |
| Testing | pytest + pytest-asyncio |
| Containerization | Docker (Week 4) |
| CI/CD | GitHub Actions (Week 4) |
| Cloud | GCP Cloud Run (Week 5) |

---

## Local Setup

### Prerequisites
- Python 3.11+

### Install

```bash
git clone https://github.com/xiaoyingbao/autoagent.git
cd autoagent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Run

```bash
uvicorn main:app --reload
```

### Test

```bash
pytest tests/ -v
```

### API Docs

Open http://127.0.0.1:8000/docs in your browser.

### Example Query

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Should our startup use MySQL or PostgreSQL for a food delivery platform with 100K daily users?"}'
```

---

## Project Milestones

| Week | Milestone | Status |
|------|-----------|--------|
| 1 | Project setup, FastAPI skeleton | ✅ Done |
| 2 | Planner + basic Executor | ✅ Done |
| 3 | Full pipeline + Reviewer + DB + tests | ✅ Done |
| 4 | Redis queue + Docker + CI/CD | 🔲 Upcoming |
| 5 | GCP Cloud Run deployment | 🔲 Upcoming |
| 6 | Streamlit UI + demo prep | 🔲 Upcoming |
| 7 | Final demo | 🔲 Upcoming |
