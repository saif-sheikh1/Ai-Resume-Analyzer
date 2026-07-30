"""
Resume service — business logic for resume upload, parsing, and analysis.
"""
from uuid import UUID

from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.models.analysis import Analysis
from app.repositories.resume_repo import ResumeRepository
from app.repositories.analysis_repo import AnalysisRepository
from app.services.storage_service import StorageService
from app.services.parser_service import parse_resume
from app.services.ats_service import calculate_ats_score
from app.services import ai_service
from app.core.logging import get_logger

logger = get_logger(__name__)


class ResumeService:
    def __init__(self, db: Session):
        self.db = db
        self.resume_repo = ResumeRepository(db)
        self.analysis_repo = AnalysisRepository(db)
        self.storage = StorageService()

    async def upload_and_parse(self, file: UploadFile, user_id: UUID) -> Resume:
        """Upload a resume file, parse it, and store in database."""
        # Upload to Supabase Storage
        upload_result = await self.storage.upload_file(file, str(user_id))

        # Parse the resume
        parse_result = parse_resume(
            upload_result["content"],
            upload_result["file_type"]
        )

        # Create resume record
        resume = Resume(
            user_id=user_id,
            filename=upload_result["filename"],
            file_url=upload_result["file_url"],
            file_type=upload_result["file_type"],
            file_size=upload_result["file_size"],
            raw_text=parse_result.get("raw_text", ""),
            parsed_data=parse_result.get("parsed_data", {}),
        )

        resume = self.resume_repo.create(resume)
        logger.info(f"Resume uploaded and parsed: {resume.id}")
        return resume

    async def analyze(self, resume_id: UUID, user_id: UUID) -> Analysis:
        """Run full ATS + AI analysis on a resume."""
        resume = self.resume_repo.get_by_id_and_user(resume_id, user_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )

        if not resume.raw_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Resume text could not be extracted. Please upload a different file."
            )

        parsed_data = resume.parsed_data or {}

        # Calculate ATS score
        ats_result = calculate_ats_score(resume.raw_text, parsed_data)

        # Run AI analysis
        try:
            ai_result = await ai_service.analyze_resume(resume.raw_text, parsed_data)
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            ai_result = {
                "ai_summary": "AI analysis could not be completed at this time.",
                "strengths": [],
                "weaknesses": [],
                "missing_skills": [],
                "formatting_suggestions": [],
                "grammar_improvements": [],
                "improved_bullets": [],
                "career_advice": "",
            }

        # Create analysis record
        analysis = Analysis(
            resume_id=resume_id,
            user_id=user_id,
            ats_score=ats_result["overall_score"],
            section_scores=ats_result["section_scores"],
            ai_summary=ai_result.get("ai_summary", ""),
            strengths=ai_result.get("strengths", []),
            weaknesses=ai_result.get("weaknesses", []),
            suggestions=ats_result["suggestions"] + ai_result.get("formatting_suggestions", []),
            missing_skills=ai_result.get("missing_skills", []) + ats_result.get("missing_keywords", []),
            improved_bullets=ai_result.get("improved_bullets", []),
            career_advice=ai_result.get("career_advice", ""),
            formatting_suggestions=ai_result.get("formatting_suggestions", []),
            grammar_improvements=ai_result.get("grammar_improvements", []),
        )

        analysis = self.analysis_repo.create(analysis)
        logger.info(f"Analysis completed: {analysis.id} (ATS: {analysis.ats_score})")
        return analysis

    def get_resume(self, resume_id: UUID, user_id: UUID) -> Resume:
        resume = self.resume_repo.get_by_id_and_user(resume_id, user_id)
        if not resume:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
        return resume

    def get_all_resumes(self, user_id: UUID, skip: int = 0, limit: int = 50) -> list[Resume]:
        return self.resume_repo.get_all_by_user(user_id, skip, limit)

    def delete_resume(self, resume_id: UUID, user_id: UUID) -> None:
        resume = self.resume_repo.get_by_id_and_user(resume_id, user_id)
        if not resume:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

        # Delete file from storage
        if resume.file_url:
            storage_path = resume.file_url.split(f"/{self.storage.bucket}/")[-1] if self.storage.bucket in resume.file_url else ""
            if storage_path:
                self.storage.delete_file(storage_path)

        self.resume_repo.delete(resume)
        logger.info(f"Resume deleted: {resume_id}")
