from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.routes import router
from db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("AutoAgent started. Database ready.")
    yield


app = FastAPI(
    title="AutoAgent",
    description=(
        "A production-grade multi-agent LLM orchestration system. "
        "Three specialized agents (Planner → Executor → Reviewer) "
        "collaborate to solve complex technical decision queries."
    ),
    version="0.3.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health", tags=["System"])
async def health():
    return {
        "status": "ok",
        "version": "0.3.0",
        "pipeline": ["planner", "executor", "reviewer"],
        "storage": "postgresql",
    }


