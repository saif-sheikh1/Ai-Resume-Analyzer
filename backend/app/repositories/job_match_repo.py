"""
JobMatch repository — data access layer for job match operations.
"""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.job_match import JobMatch


class JobMatchRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, match_id: UUID) -> Optional[JobMatch]:
        return self.db.query(JobMatch).filter(JobMatch.id == match_id).first()

    def get_by_id_and_user(self, match_id: UUID, user_id: UUID) -> Optional[JobMatch]:
        return self.db.query(JobMatch).filter(
            JobMatch.id == match_id,
            JobMatch.user_id == user_id
        ).first()

    def get_all_by_user(self, user_id: UUID, skip: int = 0, limit: int = 50) -> list[JobMatch]:
        return (
            self.db.query(JobMatch)
            .filter(JobMatch.user_id == user_id)
            .order_by(desc(JobMatch.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_resume(self, resume_id: UUID) -> list[JobMatch]:
        return (
            self.db.query(JobMatch)
            .filter(JobMatch.resume_id == resume_id)
            .order_by(desc(JobMatch.created_at))
            .all()
        )

    def create(self, job_match: JobMatch) -> JobMatch:
        self.db.add(job_match)
        self.db.commit()
        self.db.refresh(job_match)
        return job_match

    def update(self, job_match: JobMatch) -> JobMatch:
        self.db.commit()
        self.db.refresh(job_match)
        return job_match

    def delete(self, job_match: JobMatch) -> None:
        self.db.delete(job_match)
        self.db.commit()
