from typing import Literal

from pydantic import BaseModel, Field


class StartSessionRequest(BaseModel):
    learner_name: str = Field(default="Learner", min_length=1, max_length=120)
    level: Literal["A1", "A2", "B1", "B2", "C1", "C2"] = "B1"
    scenario: Literal["job interview", "casual chat", "business meeting"] = "casual chat"


class StartSessionResponse(BaseModel):
    session_id: str
    opening_prompt: str


class TutorTurnRequest(BaseModel):
    session_id: str
    transcript: str = Field(min_length=2, max_length=1000)


class TutorTurnResponse(BaseModel):
    session_id: str
    corrected_text: str
    grammar_notes: list[str]
    fluency_score: int
    vocabulary_tips: list[str]
    tutor_reply: str
