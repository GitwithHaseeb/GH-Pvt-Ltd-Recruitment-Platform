from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class CandidateCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = ""
    position_applied: str
    cover_letter: Optional[str] = ""


class CandidateRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    position_applied: str
    source: str
    ats_score: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class JobPositionRead(BaseModel):
    id: int
    title: str
    description: str
    required_skills: dict
    experience_years: int
    education: str

    class Config:
        from_attributes = True


class MetricsResponse(BaseModel):
    total_candidates: int
    source_split: dict[str, int]
    ats_distribution: list[float]
    top_candidates: list[CandidateRead]
    selected_candidates: list[CandidateRead]
    email_logs: list[dict]


class RunPipelineResponse(BaseModel):
    message: str
    selected_mapping: dict[str, int] = Field(default_factory=dict)
