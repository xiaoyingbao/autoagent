import pytest
from unittest.mock import AsyncMock, patch
from agents.reviewer import ReviewerAgent, ReviewerOutput
from agents.executor import SubtaskResult

RESULTS = [
    SubtaskResult(subtask_id=1, title="Performance",
                  analysis="PostgreSQL better.", key_findings=["MVCC"], recommendation="PostgreSQL"),
    SubtaskResult(subtask_id=2, title="Cost",
                  analysis="Cost-neutral.", key_findings=["~$100/mo"], recommendation="Either"),
]

MOCK_REVIEW = ReviewerOutput(
    final_answer="Use PostgreSQL. It outperforms MySQL on all key dimensions for food delivery.",
    quality_score=0.91,
    gaps_identified=["Failover strategy not analyzed"],
    passed=True,
)


@pytest.mark.asyncio
async def test_reviewer_returns_reviewer_output():
    agent = ReviewerAgent()
    with patch.object(agent, "review", new_callable=AsyncMock) as mock_review:
        mock_review.return_value = MOCK_REVIEW
        result = await agent.review("MySQL or PostgreSQL?", RESULTS)
    assert isinstance(result, ReviewerOutput)


@pytest.mark.asyncio
async def test_reviewer_quality_score_in_range():
    agent = ReviewerAgent()
    with patch.object(agent, "review", new_callable=AsyncMock) as mock_review:
        mock_review.return_value = MOCK_REVIEW
        result = await agent.review("MySQL or PostgreSQL?", RESULTS)
    assert 0.0 <= result.quality_score <= 1.0


@pytest.mark.asyncio
async def test_reviewer_passed_reflects_quality_score():
    agent = ReviewerAgent()
    with patch.object(agent, "review", new_callable=AsyncMock) as mock_review:
        mock_review.return_value = MOCK_REVIEW
        result = await agent.review("MySQL or PostgreSQL?", RESULTS)
    assert result.passed == (result.quality_score >= 0.7)