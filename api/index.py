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

from app.main import app
