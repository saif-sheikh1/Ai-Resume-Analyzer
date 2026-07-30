"""
Pydantic schemas for analysis results.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class AnalysisResponse(BaseModel):
    id: UUID
    resume_id: UUID
    user_id: UUID
    ats_score: Optional[float] = None
    section_scores: Optional[dict] = None
    ai_summary: Optional[str] = None
    strengths: Optional[list[str]] = None
    weaknesses: Optional[list[str]] = None
    suggestions: Optional[list[str]] = None
    missing_skills: Optional[list[str]] = None
    improved_bullets: Optional[list[str]] = None
    career_advice: Optional[str] = None
    formatting_suggestions: Optional[list[str]] = None
    grammar_improvements: Optional[list[str]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AnalysisListResponse(BaseModel):
    id: UUID
    resume_id: UUID
    ats_score: Optional[float] = None
    ai_summary: Optional[str] = None
    created_at: datetime
    resume_filename: Optional[str] = None

    class Config:
        from_attributes = True


class ATSScoreBreakdown(BaseModel):
    overall_score: float
    contact_info: float
    formatting: float
    skills: float
    experience: float
    education: float
    keywords: float
    projects: float
    grammar: float
    missing_keywords: list[str] = []
    suggestions: list[str] = []


class DashboardStats(BaseModel):
    total_resumes: int = 0
    total_analyses: int = 0
    average_ats_score: float = 0.0
    highest_ats_score: float = 0.0
    recent_analyses: list[AnalysisListResponse] = []
    score_history: list[dict] = []
