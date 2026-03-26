import asyncio
import logging
from pipeline.celery_app import celery_app
from pipeline.orchestrator import Orchestrator

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, name="run_pipeline_task", max_retries=2)
def run_pipeline_task(self, query: str) -> dict:
    """
    Celery task wrapping the async Orchestrator.
    asyncio.run() bridges Celery (sync) → Orchestrator (async).
    """
    try:
        result = asyncio.run(_run(query))
        return result
    except Exception as exc:
        logger.error(f"Pipeline task failed: {exc}")
        raise self.retry(exc=exc, countdown=5)

async def _run(query: str) -> dict:
    orch = Orchestrator()
    resp = await orch.run(query)
    return {
        "task_id": resp.task_id,
        "status": "completed",
        "subtasks_count": resp.subtasks_count,
        "final_answer": resp.final_answer,
        "quality_score": resp.quality_score,
        "passed": resp.passed,
        "duration_seconds": resp.duration_seconds,
    }


