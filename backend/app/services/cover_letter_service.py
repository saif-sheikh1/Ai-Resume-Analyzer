"""
Cover Letter service — generates AI cover letters.
"""
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.resume_repo import ResumeRepository
from app.repositories.job_match_repo import JobMatchRepository
from app.services import ai_service
from app.core.logging import get_logger

logger = get_logger(__name__)


class CoverLetterService:
    def __init__(self, db: Session):
        self.db = db
        self.resume_repo = ResumeRepository(db)
        self.match_repo = JobMatchRepository(db)

    async def generate(
        self, resume_id: UUID, user_id: UUID,
        job_description: str, company_name: str, position: str,
        tone: str = "professional"
    ) -> dict:
        """Generate a cover letter using AI."""
        resume = self.resume_repo.get_by_id_and_user(resume_id, user_id)
        if not resume:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

        parsed_data = resume.parsed_data or {}
        raw_text = resume.raw_text or f"Candidate name: {parsed_data.get('name', 'Applicant')}. Skills: {', '.join(parsed_data.get('skills', []))}"

        cover_letter = await ai_service.generate_cover_letter(
            raw_text, parsed_data,
            job_description, company_name, position, tone
        )

        logger.info(f"Cover letter generated for resume {resume_id}")
        return {"cover_letter": cover_letter}
