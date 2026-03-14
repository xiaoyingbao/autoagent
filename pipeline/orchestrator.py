import uuid
from datetime import datetime
from typing import List
from pydantic import BaseModel
from agents.planner import PlannerAgent, PlannerOutput
from agents.executor import ExecutorAgent, SubtaskResult
from agents.reviewer import ReviewerAgent, ReviewerOutput
from db.database import AsyncSessionLocal
from db.models import Task, SubtaskLog


class PipelineRequest(BaseModel):
    query: str


class PipelineResponse(BaseModel):
    task_id: str
    original_query: str
    subtasks_count: int
    final_answer: str
    quality_score: float
    passed: bool
    gaps: List[str]
    duration_seconds: float


class Orchestrator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.reviewer = ReviewerAgent()

    async def run(self, query: str) -> PipelineResponse:
        task_id = str(uuid.uuid4())
        started_at = datetime.utcnow()

        # Step 1 — Planner: decompose query into subtasks
        plan: PlannerOutput = await self.planner.plan(query)

        # Step 2 — Executor: analyze each subtask independently
        # Note: sequential now; Week 4 upgrades to parallel via Celery
        results: List[SubtaskResult] = await self.executor.execute_all(plan.subtasks)

        # Step 3 — Reviewer: validate, score, and consolidate
        review: ReviewerOutput = await self.reviewer.review(query, results)

        duration = (datetime.utcnow() - started_at).total_seconds()

        # Step 4 — Persist full task record to PostgreSQL
        await self._persist(task_id, query, plan, results, review, duration)

        return PipelineResponse(
            task_id=task_id,
            original_query=query,
            subtasks_count=len(plan.subtasks),
            final_answer=review.final_answer,
            quality_score=review.quality_score,
            passed=review.passed,
            gaps=review.gaps_identified,
            duration_seconds=round(duration, 2),
        )

    async def _persist(self, task_id, query, plan, results, review, duration):
        """Persist task + all subtask logs to PostgreSQL."""
        try:
            async with AsyncSessionLocal() as db:
                db.add(Task(
                    id=task_id,
                    query=query,
                    subtasks_count=len(plan.subtasks),
                    final_answer=review.final_answer,
                    quality_score=review.quality_score,
                    passed=review.passed,
                    duration_seconds=duration,
                ))
                for r in results:
                    db.add(SubtaskLog(
                        task_id=task_id,
                        subtask_id=r.subtask_id,
                        title=r.title,
                        analysis=r.analysis,
                        recommendation=r.recommendation,
                    ))
                await db.commit()
        except Exception as e:
            # DB failure must not break the API response
            print(f"[WARN] DB persist failed: {e}")

