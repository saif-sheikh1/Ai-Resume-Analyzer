"""
Models package — import all models so Alembic can discover them.
"""
from app.models.user import User
from app.models.resume import Resume
from app.models.analysis import Analysis
from app.models.job_match import JobMatch

__all__ = ["User", "Resume", "Analysis", "JobMatch"]
