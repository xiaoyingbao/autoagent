import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from config import settings
from agents.executor import SubtaskResult


class ReviewerOutput(BaseModel):
    final_answer: str
    quality_score: float = Field(ge=0.0, le=1.0)
    gaps_identified: List[str]
    passed: bool  # True if quality_score >= 0.7


REVIEWER_SYSTEM = """You are a senior technical reviewer. You receive a user's original \
query and the analysis results from multiple executor agents. Your responsibilities:

1. Validate each result for accuracy, completeness, and internal consistency
2. Identify gaps, contradictions, or missing perspectives
3. Synthesize all results into one clear, comprehensive, well-structured final answer
4. Score overall quality from 0.0 to 1.0 (passed = score >= 0.7)

Return ONLY valid JSON with no markdown. You MUST use exactly these field names:
{{
  "final_answer": "<your comprehensive consolidated answer as a single string>",
  "quality_score": 0.9,
  "gaps_identified": ["<gap 1>", "<gap 2>"],
  "passed": true
}}

IMPORTANT: final_answer must be a single string, not an object or dict."""


class ReviewerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.model_name,
            api_key=settings.openai_api_key,
            temperature=0.1,
            max_tokens=settings.max_tokens,
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", REVIEWER_SYSTEM),
            ("human", (
                "Original query: {original_query}\n\n"
                "Executor results:\n{executor_results}\n\n"
                "Review, validate, and consolidate into a final answer:"
            )),
        ])

    async def review(self, original_query: str, results: List[SubtaskResult]) -> ReviewerOutput:
        results_text = "\n\n".join([
            f"[Subtask {r.subtask_id}: {r.title}]\n"
            f"Analysis: {r.analysis}\n"
            f"Key findings: {' | '.join(r.key_findings)}\n"
            f"Recommendation: {r.recommendation}"
            for r in results
        ])
        chain = self.prompt | self.llm
        response = await chain.ainvoke({
            "original_query": original_query,
            "executor_results": results_text,
        })
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            raw = raw[4:] if raw.startswith("json") else raw
        data = json.loads(raw.strip())
        # enforce passed rule
        data["passed"] = data.get("quality_score", 0) >= 0.7
        return ReviewerOutput(**data)



