from sqlalchemy import Column, String, Float, Boolean, Integer, Text, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Task(Base):
    """Top-level task record: one row per /query call."""
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)           # UUID
    query = Column(Text, nullable=False)            # original user query
    subtasks_count = Column(Integer)                # how many subtasks Planner created
    final_answer = Column(Text)                     # Reviewer's consolidated answer
    quality_score = Column(Float)                   # Reviewer quality score 0.0-1.0
    passed = Column(Boolean)                        # quality_score >= 0.7
    duration_seconds = Column(Float)               # end-to-end latency
    created_at = Column(DateTime, default=datetime.utcnow)


class SubtaskLog(Base):
    """One row per subtask per task — full audit trail of Executor outputs."""
    __tablename__ = "subtask_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String, nullable=False)        # FK → tasks.id
    subtask_id = Column(Integer)                    # 1, 2, 3...
    title = Column(String)
    analysis = Column(Text)
    recommendation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


