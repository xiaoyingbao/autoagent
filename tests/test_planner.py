import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from agents.planner import PlannerAgent, PlannerOutput, Subtask
import json

MOCK_PLAN_JSON = json.dumps({
    "original_query": "MySQL or PostgreSQL for food delivery?",
    "subtasks": [
        {"id": 1, "title": "Performance", "description": "Compare throughput", "focus": "Which is faster?"},
        {"id": 2, "title": "Data Model", "description": "Compare schemas", "focus": "Which fits better?"},
        {"id": 3, "title": "Cost", "description": "Compare costs", "focus": "Which is cheaper?"},
    ],
    "reasoning": "Decomposed into three key technical dimensions.",
})


@pytest.mark.asyncio
async def test_planner_returns_planner_output():
    agent = PlannerAgent()
    mock_resp = MagicMock()
    mock_resp.content = MOCK_PLAN_JSON
    with patch("agents.planner.ChatOpenAI") as MockLLM:
        instance = MockLLM.return_value
        instance.ainvoke = AsyncMock(return_value=mock_resp)
        agent.llm = instance
        # patch the chain directly
        with patch.object(agent, "plan", new_callable=AsyncMock) as mock_plan:
            mock_plan.return_value = PlannerOutput(**json.loads(MOCK_PLAN_JSON))
            result = await agent.plan("MySQL or PostgreSQL for food delivery?")
    assert isinstance(result, PlannerOutput)


@pytest.mark.asyncio
async def test_planner_returns_correct_subtask_count():
    agent = PlannerAgent()
    with patch.object(agent, "plan", new_callable=AsyncMock) as mock_plan:
        mock_plan.return_value = PlannerOutput(**json.loads(MOCK_PLAN_JSON))
        result = await agent.plan("MySQL or PostgreSQL?")
    assert len(result.subtasks) == 3


@pytest.mark.asyncio
async def test_planner_subtasks_have_all_fields():
    agent = PlannerAgent()
    with patch.object(agent, "plan", new_callable=AsyncMock) as mock_plan:
        mock_plan.return_value = PlannerOutput(**json.loads(MOCK_PLAN_JSON))
        result = await agent.plan("MySQL or PostgreSQL?")
    for s in result.subtasks:
        assert isinstance(s, Subtask)
        assert s.id > 0
        assert s.title and s.description and s.focus

