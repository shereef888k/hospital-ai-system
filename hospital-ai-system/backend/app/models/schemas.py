from pydantic import BaseModel
from typing import List, Optional


class TriageRequest(BaseModel):
    age: int
    gender: str
    symptoms: List[str]
    duration_days: int


class TextTriageRequest(BaseModel):
    text: str
    age: int = 30
    gender: str = "male"
    duration_days: int = 1


class TriageResponse(BaseModel):
    urgency: str
    department: str
    advice: str
    source: str
    score: Optional[int] = None
    confidence: Optional[float] = None
    factors: List[str] = []