"""
JobMatch model for storing job description comparisons.
"""
import uuid
from sqlalchemy import Column, String, Text, JSON, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class JobMatch(Base, TimestampMixin):
    __tablename__ = "job_matches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Job Description
    job_title = Column(String(255), nullable=True)
    company_name = Column(String(255), nullable=True)
    job_description = Column(Text, nullable=False)

    # Match Results
    match_percentage = Column(Float, nullable=True)
    matching_skills = Column(JSON, nullable=True)  # ["skill1", "skill2", ...]
    missing_skills = Column(JSON, nullable=True)  # ["skill1", "skill2", ...]
    keyword_analysis = Column(JSON, nullable=True)  # {keyword: {found: bool, importance: str}}
    hiring_probability = Column(String(50), nullable=True)  # "High", "Medium", "Low"
    recommendations = Column(JSON, nullable=True)  # ["recommendation1", ...]

    # Cover Letter
    cover_letter = Column(Text, nullable=True)

    # Interview Questions
    interview_questions = Column(JSON, nullable=True)  # {hr: [...], technical: [...], ...}

    # Relationships
    resume = relationship("Resume", back_populates="job_matches")
    user = relationship("User", back_populates="job_matches")

    def __repr__(self) -> str:
        return f"<JobMatch resume={self.resume_id} match={self.match_percentage}%>"
