"""
Pydantic schemas for job matching, cover letter, and interview prep.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class JobMatchRequest(BaseModel):
    resume_id: UUID
    job_description: str = Field(..., min_length=50)
    job_title: Optional[str] = None
    company_name: Optional[str] = None


class JobMatchResponse(BaseModel):
    id: UUID
    resume_id: UUID
    user_id: UUID
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    job_description: str
    match_percentage: Optional[float] = None
    matching_skills: Optional[list[str]] = None
    missing_skills: Optional[list[str]] = None
    keyword_analysis: Optional[dict] = None
    hiring_probability: Optional[str] = None
    recommendations: Optional[list[str]] = None
    cover_letter: Optional[str] = None
    interview_questions: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class JobMatchListResponse(BaseModel):
    id: UUID
    resume_id: UUID
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    match_percentage: Optional[float] = None
    hiring_probability: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CoverLetterRequest(BaseModel):
    resume_id: UUID
    job_description: str = Field(..., min_length=50)
    company_name: str = Field(..., min_length=1)
    position: str = Field(..., min_length=1)
    tone: str = Field(default="professional")  # professional, creative, technical


class CoverLetterResponse(BaseModel):
    cover_letter: str
    job_match_id: Optional[UUID] = None


class InterviewPrepRequest(BaseModel):
    resume_id: UUID
    job_description: Optional[str] = None
    job_title: Optional[str] = None


class InterviewQuestion(BaseModel):
    question: str
    sample_answer: str
    difficulty: str = "Medium"  # Easy, Medium, Hard
    category: str = ""  # HR, Technical, Behavioral, Coding


class InterviewPrepResponse(BaseModel):
    hr_questions: list[InterviewQuestion] = []
    technical_questions: list[InterviewQuestion] = []
    behavioral_questions: list[InterviewQuestion] = []
    coding_questions: list[InterviewQuestion] = []
    improvement_suggestions: list[str] = []
