from fastapi import APIRouter, HTTPException
from pipeline.orchestrator import Orchestrator, PipelineRequest, PipelineResponse

router = APIRouter()
_orchestrator = Orchestrator()


@router.post(
    "/query",
    response_model=PipelineResponse,
    tags=["Agent Pipeline"],
    summary="Submit a technical query to the multi-agent pipeline",
)
async def run_query(req: PipelineRequest):
    """
    Runs the full Planner → Executor → Reviewer pipeline:
    - **Planner** decomposes the query into 3-5 subtasks
    - **Executor** analyzes each subtask independently via OpenAI
    - **Reviewer** validates, scores, and consolidates into a final answer
    - Result is persisted to PostgreSQL with full task metadata
    """
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    try:
        return await _orchestrator.run(req.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


