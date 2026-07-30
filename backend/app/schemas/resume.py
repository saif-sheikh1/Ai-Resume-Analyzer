"""
Pydantic schemas for resume operations.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ResumeResponse(BaseModel):
    id: UUID
    user_id: UUID
    filename: str
    file_url: str
    file_type: str
    file_size: int
    parsed_data: Optional[dict] = None
    raw_text: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ResumeListResponse(BaseModel):
    id: UUID
    filename: str
    file_type: str
    file_size: int
    created_at: datetime
    has_analysis: bool = False
    latest_ats_score: Optional[float] = None

    class Config:
        from_attributes = True


class ParsedResumeData(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    summary: Optional[str] = None
    skills: list[str] = []
    experience: list[dict] = []
    education: list[dict] = []
    projects: list[dict] = []
    certifications: list[str] = []
    languages: list[str] = []
