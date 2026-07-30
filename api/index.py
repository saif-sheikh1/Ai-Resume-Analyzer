"""
Vercel Serverless Entry Point for FastAPI Backend.
Handles path resolution and graceful error logging for Vercel AWS Lambda.
"""
import sys
import os

# Add root directory and backend directory to sys.path for Vercel Lambda
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
backend_dir = os.path.abspath(os.path.join(current_dir, "..", "backend"))

for path in [parent_dir, backend_dir, current_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    from app.main import app
except Exception as e:
    # Fallback FastAPI app if module import fails
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    app = FastAPI(title="AI Resume Analyzer API (Error Mode)")

    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
    async def catch_all_error(path: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Backend initialization failed",
                "detail": str(e),
                "sys_path": sys.path,
                "current_dir": current_dir,
            }
        )
