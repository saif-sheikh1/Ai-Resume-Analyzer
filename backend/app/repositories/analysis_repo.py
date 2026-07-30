"""
Analysis repository — data access layer for analysis operations.
"""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, func

from app.models.analysis import Analysis
from app.models.resume import Resume


class AnalysisRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, analysis_id: UUID) -> Optional[Analysis]:
        return self.db.query(Analysis).filter(Analysis.id == analysis_id).first()

    def get_by_id_and_user(self, analysis_id: UUID, user_id: UUID) -> Optional[Analysis]:
        return self.db.query(Analysis).filter(
            Analysis.id == analysis_id,
            Analysis.user_id == user_id
        ).first()

    def get_all_by_user(self, user_id: UUID, skip: int = 0, limit: int = 50) -> list[Analysis]:
        return (
            self.db.query(Analysis)
            .filter(Analysis.user_id == user_id)
            .order_by(desc(Analysis.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_resume(self, resume_id: UUID) -> list[Analysis]:
        return (
            self.db.query(Analysis)
            .filter(Analysis.resume_id == resume_id)
            .order_by(desc(Analysis.created_at))
            .all()
        )

    def get_latest_by_resume(self, resume_id: UUID) -> Optional[Analysis]:
        return (
            self.db.query(Analysis)
            .filter(Analysis.resume_id == resume_id)
            .order_by(desc(Analysis.created_at))
            .first()
        )

    def count_by_user(self, user_id: UUID) -> int:
        return self.db.query(Analysis).filter(Analysis.user_id == user_id).count()

    def average_score_by_user(self, user_id: UUID) -> float:
        result = (
            self.db.query(func.avg(Analysis.ats_score))
            .filter(Analysis.user_id == user_id, Analysis.ats_score.isnot(None))
            .scalar()
        )
        return round(float(result), 1) if result else 0.0

    def highest_score_by_user(self, user_id: UUID) -> float:
        result = (
            self.db.query(func.max(Analysis.ats_score))
            .filter(Analysis.user_id == user_id, Analysis.ats_score.isnot(None))
            .scalar()
        )
        return round(float(result), 1) if result else 0.0

    def get_recent_by_user(self, user_id: UUID, limit: int = 5) -> list[Analysis]:
        return (
            self.db.query(Analysis)
            .options(joinedload(Analysis.resume))
            .filter(Analysis.user_id == user_id)
            .order_by(desc(Analysis.created_at))
            .limit(limit)
            .all()
        )

    def get_score_history(self, user_id: UUID, limit: int = 20) -> list[dict]:
        results = (
            self.db.query(Analysis.ats_score, Analysis.created_at, Resume.filename)
            .join(Resume, Analysis.resume_id == Resume.id)
            .filter(Analysis.user_id == user_id, Analysis.ats_score.isnot(None))
            .order_by(Analysis.created_at)
            .limit(limit)
            .all()
        )
        return [
            {"score": r[0], "date": r[1].isoformat(), "filename": r[2]}
            for r in results
        ]

    def create(self, analysis: Analysis) -> Analysis:
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    def update(self, analysis: Analysis) -> Analysis:
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    def delete(self, analysis: Analysis) -> None:
        self.db.delete(analysis)
        self.db.commit()
