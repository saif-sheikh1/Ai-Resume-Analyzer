"""
SQLAlchemy database engine and session configuration.
Optimized for serverless environments (Vercel) and Supabase PostgreSQL.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# Create synchronous engine optimized for serverless functions
engine = create_engine(
    settings.sync_database_url,
    pool_size=3,
    max_overflow=5,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"connect_timeout": 5},
    echo=settings.DEBUG,
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db() -> Session:
    """Dependency that provides a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
