"""
FastAPI application entry point.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.api.routes import auth, users, resume, analysis, job_match, reports

# Setup logging
setup_logging(debug=settings.DEBUG)
logger = get_logger(__name__)

# Rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info("🚀 AI Resume Analyzer API starting up...")
    logger.info(f"   Frontend URL: {settings.FRONTEND_URL}")
    logger.info(f"   Debug mode: {settings.DEBUG}")

    # Create tables only in local DEBUG mode to keep serverless cold starts under 100ms
    if settings.DEBUG:
        try:
            from app.db.base import Base
            from app.db.session import engine
            from app.models import User, Resume, Analysis, JobMatch  # noqa: F401
            Base.metadata.create_all(bind=engine)
            logger.info("   Database tables ensured (DEBUG mode)")
        except Exception as e:
            logger.warning(f"   Database table creation skipped: {e}")

    yield

    logger.info("👋 AI Resume Analyzer API shutting down...")


# Create FastAPI app
app = FastAPI(
    title="AI Resume Analyzer API",
    description="AI-powered resume analysis, ATS scoring, job matching, and career advice platform.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS — Allow all local, Vercel, Render, and custom domain origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=r"https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred", "error": str(exc)},
    )


# Register routers
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(resume.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")
app.include_router(job_match.router, prefix="/api")
app.include_router(reports.router, prefix="/api")


# Health check
@app.get("/api/health", tags=["Health"])
def health_check():
    """API health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/", tags=["Root"])
def root():
    """Root endpoint."""
    return {
        "name": "AI Resume Analyzer API",
        "version": "1.0.0",
        "docs": "/docs",
    }
