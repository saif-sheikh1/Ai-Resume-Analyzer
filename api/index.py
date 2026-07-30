"""
Vercel Serverless Entry Point for FastAPI Backend.
"""
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.main import app

# Vercel serverless requires `app` object exposed
