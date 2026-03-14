import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from config import settings


class Subtask(BaseModel):
    id: int = Field(description="Subtask index starting from 1")
    title: str = Field(description="Short title of this subtask")
    description: str = Field(description="Detailed description of what to analyze")
    focus: str = Field(description="Key question this subtask should answer")


class PlannerOutput(BaseModel):
    original_query: str
    subtasks: List[Subtask]
    reasoning: str


PLANNER_SYSTEM = """You are a senior technical planning agent. Your job is to decompose \
complex technical questions into 3-5 focused, non-overlapping subtasks that together \
provide a comprehensive answer.

Return ONLY valid JSON with no markdown, no explanation, strictly this schema:
{{
  "original_query": "<the original question>",
  "subtasks": [
    {{
      "id": 1,
      "title": "<short title>",
      "description": "<what to analyze>",
      "focus": "<key question to answer>"
    }}
  ],
  "reasoning": "<why you decomposed it this way>"
}}"""


class PlannerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.model_name,
            api_key=settings.openai_api_key,
            temperature=0.2,
            max_tokens=settings.max_tokens,
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", PLANNER_SYSTEM),
            ("human", "Decompose this technical query:\n\n{query}"),
        ])

    async def plan(self, query: str) -> PlannerOutput:
        chain = self.prompt | self.llm
        response = await chain.ainvoke({"query": query})
        raw = response.content.strip()
        # strip accidental markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            raw = raw[4:] if raw.startswith("json") else raw
        data = json.loads(raw.strip())
        return PlannerOutput(**data)
