import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from agents.executor import ExecutorAgent, SubtaskResult
from agents.planner import Subtask
import json

SUBTASK = Subtask(id=1, title="Performance", description="Compare perf", focus="Which is faster?")

MOCK_RESULT = SubtaskResult(
    subtask_id=1,
    title="Performance",
    analysis="PostgreSQL outperforms MySQL on complex analytical queries.",
    key_findings=["Better query planner", "MVCC reduces lock contention"],
    recommendation="Use PostgreSQL for read-heavy workloads.",
)


@pytest.mark.asyncio
async def test_executor_returns_subtask_result():
    agent = ExecutorAgent()
    with patch.object(agent, "execute_subtask", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = MOCK_RESULT
        result = await agent.execute_subtask(SUBTASK)
    assert isinstance(result, SubtaskResult)
    assert result.subtask_id == 1


@pytest.mark.asyncio
async def test_executor_result_has_findings_and_recommendation():
    agent = ExecutorAgent()
    with patch.object(agent, "execute_subtask", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = MOCK_RESULT
        result = await agent.execute_subtask(SUBTASK)
    assert len(result.key_findings) >= 1
    assert len(result.recommendation) > 0


@pytest.mark.asyncio
async def test_executor_processes_all_subtasks():
    subtasks = [
        Subtask(id=i, title=f"Dim {i}", description="desc", focus="focus?")
        for i in range(1, 4)
    ]
    agent = ExecutorAgent()
    with patch.object(agent, "execute_all", new_callable=AsyncMock) as mock_all:
        mock_all.return_value = [MOCK_RESULT, MOCK_RESULT, MOCK_RESULT]
        results = await agent.execute_all(subtasks)
    assert len(results) == 3
    assert all(isinstance(r, SubtaskResult) for r in results)

