"""
Job Match routes.
"""
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.job_match import (
    JobMatchRequest, JobMatchResponse, JobMatchListResponse,
    CoverLetterRequest, CoverLetterResponse,
    InterviewPrepRequest, InterviewPrepResponse,
)
from app.schemas.auth import MessageResponse
from app.services.job_match_service import JobMatchService
from app.services.cover_letter_service import CoverLetterService
from app.services.interview_service import InterviewService

router = APIRouter(prefix="/job-match", tags=["Job Match"])


@router.post("/", response_model=JobMatchResponse, status_code=201)
async def create_job_match(
    data: JobMatchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Compare a resume against a job description."""
    service = JobMatchService(db)
    return await service.match(
        resume_id=data.resume_id,
        user_id=current_user.id,
        job_description=data.job_description,
        job_title=data.job_title,
        company_name=data.company_name,
    )


@router.get("/", response_model=list[JobMatchListResponse])
def list_job_matches(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all job matches for the current user."""
    service = JobMatchService(db)
    return service.get_all_matches(current_user.id, skip, limit)


@router.get("/{match_id}", response_model=JobMatchResponse)
def get_job_match(
    match_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific job match result."""
    service = JobMatchService(db)
    return service.get_match(match_id, current_user.id)


@router.delete("/{match_id}", response_model=MessageResponse)
def delete_job_match(
    match_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a job match."""
    service = JobMatchService(db)
    service.delete_match(match_id, current_user.id)
    return MessageResponse(message="Job match deleted successfully")


@router.post("/cover-letter", response_model=CoverLetterResponse)
async def generate_cover_letter(
    data: CoverLetterRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate an AI cover letter based on resume and job description."""
    service = CoverLetterService(db)
    result = await service.generate(
        resume_id=data.resume_id,
        user_id=current_user.id,
        job_description=data.job_description,
        company_name=data.company_name,
        position=data.position,
        tone=data.tone,
    )
    return CoverLetterResponse(cover_letter=result["cover_letter"])


@router.post("/interview-prep", response_model=InterviewPrepResponse)
async def generate_interview_prep(
    data: InterviewPrepRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate AI interview preparation questions."""
    service = InterviewService(db)
    result = await service.generate_questions(
        resume_id=data.resume_id,
        user_id=current_user.id,
        job_description=data.job_description,
        job_title=data.job_title,
    )
    return result
