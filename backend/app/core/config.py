"""
Application configuration loaded from environment variables.
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings read from environment variables."""

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:Airesume%40123@db.jzwuentvficzlzqsbtcv.supabase.co:5432/postgres")

    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "https://jzwuentvficzlzqsbtcv.supabase.co")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp6d3VlbnR2Zmljemx6cXNidGN2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUzOTgwMjEsImV4cCI6MjEwMDk3NDAyMX0.sszUHDATmjssgrr5qOGTENrboIfju7ceD2aJsZZjQPc")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp6d3VlbnR2Zmljemx6cXNidGN2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NTM5ODAyMSwiZXhwIjoyMTAwOTc0MDIxfQ.lI_RBfjfqzP2vysYvO8cGd18bdSnFrTa8hxcCvHhpSk")

    # Google Gemini AI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6LQXvgR0U4ORYMc3ahorCgocKRoyiIiD3cwcj1rXWJtGA")

    # JWT Authentication
    JWT_SECRET: str = os.getenv("JWT_SECRET", "ai-resume-analyzer-jwt-secret-key-2026-production-secure")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Application URLs
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_URL: str = "http://localhost:8000"

    # Server
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    DEBUG: bool = False

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Supabase Storage
    STORAGE_BUCKET: str = "resumes"

    @property
    def async_database_url(self) -> str:
        """Convert sync postgres URL to async (asyncpg)."""
        if self.DATABASE_URL.startswith("postgresql://"):
            return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
        return self.DATABASE_URL

    @property
    def sync_database_url(self) -> str:
        """Ensure sync postgres URL uses psycopg2."""
        if self.DATABASE_URL.startswith("postgresql://"):
            return self.DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
        return self.DATABASE_URL

    class Config:
        env_file = ("backend/.env", ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
