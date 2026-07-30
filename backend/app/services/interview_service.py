"""
Interview Preparation service — generates AI-powered interview questions.
"""
from uuid import UUID
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.resume_repo import ResumeRepository
from app.services import ai_service
from app.core.logging import get_logger

logger = get_logger(__name__)


class InterviewService:
    def __init__(self, db: Session):
        self.db = db
        self.resume_repo = ResumeRepository(db)

    async def generate_questions(
        self, resume_id: UUID, user_id: UUID,
        job_description: Optional[str] = None,
        job_title: Optional[str] = None,
    ) -> dict:
        """Generate interview preparation questions using AI."""
        resume = self.resume_repo.get_by_id_and_user(resume_id, user_id)
        if not resume:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

        parsed_data = resume.parsed_data or {}
        raw_text = resume.raw_text or f"Candidate name: {parsed_data.get('name', 'Applicant')}. Skills: {', '.join(parsed_data.get('skills', []))}"

        result = await ai_service.generate_interview_questions(
            raw_text, parsed_data,
            job_description, job_title
        )

        logger.info(f"Interview questions generated for resume {resume_id}")
        return result
