import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport
from main import app
from pipeline.orchestrator import PipelineResponse

MOCK_RESPONSE = PipelineResponse(
    task_id="test-uuid-1234",
    original_query="MySQL or PostgreSQL for food delivery?",
    subtasks_count=3,
    final_answer="Use PostgreSQL. It is the better choice for this use case.",
    quality_score=0.91,
    passed=True,
    gaps=["Failover strategy not analyzed"],
    duration_seconds=4.2,
)


@pytest.mark.asyncio
async def test_health_returns_ok():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_query_returns_200():
    from pipeline.orchestrator import Orchestrator
    with patch.object(Orchestrator, "run", new_callable=AsyncMock, return_value=MOCK_RESPONSE):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            resp = await c.post("/query", json={"query": "MySQL or PostgreSQL for food delivery?"})
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_query_response_has_required_fields():
    from pipeline.orchestrator import Orchestrator
    with patch.object(Orchestrator, "run", new_callable=AsyncMock, return_value=MOCK_RESPONSE):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            resp = await c.post("/query", json={"query": "MySQL or PostgreSQL?"})
    data = resp.json()
    for field in ["task_id", "final_answer", "quality_score", "subtasks_count", "passed", "gaps"]:
        assert field in data


@pytest.mark.asyncio
async def test_empty_query_returns_400():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.post("/query", json={"query": "   "})
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_passed_true_when_quality_high():
    from pipeline.orchestrator import Orchestrator
    with patch.object(Orchestrator, "run", new_callable=AsyncMock, return_value=MOCK_RESPONSE):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            resp = await c.post("/query", json={"query": "MySQL or PostgreSQL?"})
    assert resp.json()["passed"] is True


