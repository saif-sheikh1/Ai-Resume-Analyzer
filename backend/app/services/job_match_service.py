"""
Job Match service — business logic for resume-JD comparison.
"""
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.job_match import JobMatch
from app.repositories.resume_repo import ResumeRepository
from app.repositories.job_match_repo import JobMatchRepository
from app.services import ai_service
from app.core.logging import get_logger

logger = get_logger(__name__)


class JobMatchService:
    def __init__(self, db: Session):
        self.db = db
        self.resume_repo = ResumeRepository(db)
        self.match_repo = JobMatchRepository(db)

    async def match(
        self, resume_id: UUID, user_id: UUID,
        job_description: str, job_title: str = None, company_name: str = None
    ) -> JobMatch:
        """Compare a resume against a job description."""
        resume = self.resume_repo.get_by_id_and_user(resume_id, user_id)
        if not resume:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

        if not resume.raw_text:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resume text not available")

        parsed_data = resume.parsed_data or {}

        # AI-powered match analysis
        match_result = await ai_service.analyze_job_match(
            resume.raw_text, parsed_data, job_description
        )

        # Create job match record
        job_match = JobMatch(
            resume_id=resume_id,
            user_id=user_id,
            job_title=job_title,
            company_name=company_name,
            job_description=job_description,
            match_percentage=match_result.get("match_percentage", 0),
            matching_skills=match_result.get("matching_skills", []),
            missing_skills=match_result.get("missing_skills", []),
            keyword_analysis=match_result.get("keyword_analysis", {}),
            hiring_probability=match_result.get("hiring_probability", "Medium"),
            recommendations=match_result.get("recommendations", []),
        )

        job_match = self.match_repo.create(job_match)
        logger.info(f"Job match completed: {job_match.id} ({job_match.match_percentage}%)")
        return job_match

    def get_match(self, match_id: UUID, user_id: UUID) -> JobMatch:
        match = self.match_repo.get_by_id_and_user(match_id, user_id)
        if not match:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job match not found")
        return match

    def get_all_matches(self, user_id: UUID, skip: int = 0, limit: int = 50) -> list[JobMatch]:
        return self.match_repo.get_all_by_user(user_id, skip, limit)

    def delete_match(self, match_id: UUID, user_id: UUID) -> None:
        match = self.match_repo.get_by_id_and_user(match_id, user_id)
        if not match:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job match not found")
        self.match_repo.delete(match)
