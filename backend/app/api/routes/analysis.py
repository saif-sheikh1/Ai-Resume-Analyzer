"""
Analysis routes — ATS scoring and AI analysis.
"""
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.analysis import AnalysisResponse, AnalysisListResponse, DashboardStats
from app.schemas.auth import MessageResponse
from app.services.resume_service import ResumeService
from app.repositories.analysis_repo import AnalysisRepository
from app.repositories.resume_repo import ResumeRepository
from fastapi import HTTPException, status

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.post("/{resume_id}", response_model=AnalysisResponse, status_code=201)
async def analyze_resume(
    resume_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Run ATS + AI analysis on a resume."""
    service = ResumeService(db)
    analysis = await service.analyze(resume_id, current_user.id)
    return analysis


@router.get("/", response_model=list[AnalysisListResponse])
def list_analyses(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all analyses for the current user."""
    repo = AnalysisRepository(db)
    analyses = repo.get_all_by_user(current_user.id, skip, limit)

    # Enrich with resume filename
    resume_repo = ResumeRepository(db)
    result = []
    for a in analyses:
        resume = resume_repo.get_by_id(a.resume_id)
        result.append(AnalysisListResponse(
            id=a.id,
            resume_id=a.resume_id,
            ats_score=a.ats_score,
            ai_summary=a.ai_summary[:200] if a.ai_summary else None,
            created_at=a.created_at,
            resume_filename=resume.filename if resume else None,
        ))
    return result


@router.get("/dashboard/stats", response_model=DashboardStats)
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get dashboard statistics for the current user."""
    analysis_repo = AnalysisRepository(db)
    resume_repo = ResumeRepository(db)

    # Get recent analyses with filenames
    recent = analysis_repo.get_recent_by_user(current_user.id, limit=5)
    recent_list = []
    for a in recent:
        resume = resume_repo.get_by_id(a.resume_id)
        recent_list.append(AnalysisListResponse(
            id=a.id,
            resume_id=a.resume_id,
            ats_score=a.ats_score,
            ai_summary=a.ai_summary[:200] if a.ai_summary else None,
            created_at=a.created_at,
            resume_filename=resume.filename if resume else None,
        ))

    return DashboardStats(
        total_resumes=resume_repo.count_by_user(current_user.id),
        total_analyses=analysis_repo.count_by_user(current_user.id),
        average_ats_score=analysis_repo.average_score_by_user(current_user.id),
        highest_ats_score=analysis_repo.highest_score_by_user(current_user.id),
        recent_analyses=recent_list,
        score_history=analysis_repo.get_score_history(current_user.id),
    )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific analysis by ID."""
    repo = AnalysisRepository(db)
    analysis = repo.get_by_id_and_user(analysis_id, current_user.id)
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    return analysis


@router.delete("/{analysis_id}", response_model=MessageResponse)
def delete_analysis(
    analysis_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete an analysis."""
    repo = AnalysisRepository(db)
    analysis = repo.get_by_id_and_user(analysis_id, current_user.id)
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    repo.delete(analysis)
    return MessageResponse(message="Analysis deleted successfully")
