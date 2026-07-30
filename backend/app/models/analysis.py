"""
Analysis model for storing ATS scores and AI analysis results.
"""
import uuid
from sqlalchemy import Column, String, Text, JSON, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class Analysis(Base, TimestampMixin):
    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # ATS Score
    ats_score = Column(Float, nullable=True)
    section_scores = Column(JSON, nullable=True)  # {formatting: 85, skills: 70, ...}

    # AI Analysis
    ai_summary = Column(Text, nullable=True)
    strengths = Column(JSON, nullable=True)  # ["strength1", "strength2", ...]
    weaknesses = Column(JSON, nullable=True)  # ["weakness1", "weakness2", ...]
    suggestions = Column(JSON, nullable=True)  # ["suggestion1", ...]
    missing_skills = Column(JSON, nullable=True)  # ["skill1", "skill2", ...]
    improved_bullets = Column(JSON, nullable=True)  # ["bullet1", "bullet2", ...]
    career_advice = Column(Text, nullable=True)
    formatting_suggestions = Column(JSON, nullable=True)
    grammar_improvements = Column(JSON, nullable=True)

    # Relationships
    resume = relationship("Resume", back_populates="analyses")
    user = relationship("User", back_populates="analyses")

    def __repr__(self) -> str:
        return f"<Analysis resume={self.resume_id} score={self.ats_score}>"
