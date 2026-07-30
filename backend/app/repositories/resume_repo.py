"""
Resume repository — data access layer for resume operations.
"""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.resume import Resume


class ResumeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, resume_id: UUID) -> Optional[Resume]:
        return self.db.query(Resume).filter(Resume.id == resume_id).first()

    def get_by_id_and_user(self, resume_id: UUID, user_id: UUID) -> Optional[Resume]:
        return self.db.query(Resume).filter(
            Resume.id == resume_id,
            Resume.user_id == user_id
        ).first()

    def get_all_by_user(self, user_id: UUID, skip: int = 0, limit: int = 50) -> list[Resume]:
        return (
            self.db.query(Resume)
            .filter(Resume.user_id == user_id)
            .order_by(desc(Resume.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_by_user(self, user_id: UUID) -> int:
        return self.db.query(Resume).filter(Resume.user_id == user_id).count()

    def create(self, resume: Resume) -> Resume:
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def update(self, resume: Resume) -> Resume:
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def delete(self, resume: Resume) -> None:
        self.db.delete(resume)
        self.db.commit()

    def search(self, user_id: UUID, query: str, skip: int = 0, limit: int = 50) -> list[Resume]:
        return (
            self.db.query(Resume)
            .filter(
                Resume.user_id == user_id,
                Resume.filename.ilike(f"%{query}%")
            )
            .order_by(desc(Resume.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
