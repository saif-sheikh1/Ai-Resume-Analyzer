"""
Resume upload and management routes.
"""
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.resume import ResumeResponse
from app.schemas.auth import MessageResponse
from app.services.resume_service import ResumeService

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/upload", response_model=ResumeResponse, status_code=201)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload a resume file (PDF, DOC, DOCX). Automatically parses the content."""
    service = ResumeService(db)
    resume = await service.upload_and_parse(file, current_user.id)
    return resume


@router.get("/", response_model=list[ResumeResponse])
def list_resumes(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all resumes for the current user."""
    service = ResumeService(db)
    return service.get_all_resumes(current_user.id, skip, limit)


@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific resume by ID."""
    service = ResumeService(db)
    return service.get_resume(resume_id, current_user.id)


@router.delete("/{resume_id}", response_model=MessageResponse)
def delete_resume(
    resume_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a resume and its associated file."""
    service = ResumeService(db)
    service.delete_resume(resume_id, current_user.id)
    return MessageResponse(message="Resume deleted successfully")
