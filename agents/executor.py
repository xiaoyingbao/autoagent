import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from config import settings
from agents.planner import Subtask


class SubtaskResult(BaseModel):
    subtask_id: int
    title: str
    analysis: str
    key_findings: List[str] = Field(min_length=1)
    recommendation: str


EXECUTOR_SYSTEM = """You are a technical analysis agent. You receive one focused subtask \
and must provide a thorough, structured analysis. Be specific about tradeoffs, include \
concrete numbers or examples where relevant, and give a clear actionable recommendation.

Return ONLY valid JSON with no markdown:
{{
  "subtask_id": <integer>,
  "title": "<subtask title>",
  "analysis": "<detailed analysis, 3-5 sentences>",
  "key_findings": ["<finding 1>", "<finding 2>", "<finding 3>"],
  "recommendation": "<one clear actionable recommendation>"
}}"""

class ExecutorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.model_name,
            api_key=settings.openai_api_key,
            temperature=0.3,
            max_tokens=settings.max_tokens,
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", EXECUTOR_SYSTEM),
            ("human", (
                "Subtask #{subtask_id}: {title}\n"
                "Description: {description}\n"
                "Focus question: {focus}\n\n"
                "Provide your detailed analysis:"
            )),
        ])

    async def execute_subtask(self, subtask: Subtask) -> SubtaskResult:
        chain = self.prompt | self.llm
        response = await chain.ainvoke({
            "subtask_id": subtask.id,
            "title": subtask.title,
            "description": subtask.description,
            "focus": subtask.focus,
        })
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            raw = raw[4:] if raw.startswith("json") else raw
        return SubtaskResult(**json.loads(raw.strip()))

    async def execute_all(self, subtasks: List[Subtask]) -> List[SubtaskResult]:
        """
        Execute all subtasks sequentially.
        Week 4: will be replaced with parallel async execution via Celery + Redis.
        """
        results = []
        for subtask in subtasks:
            result = await self.execute_subtask(subtask)
            results.append(result)
        return results

