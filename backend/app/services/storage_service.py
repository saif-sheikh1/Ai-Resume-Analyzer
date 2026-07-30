"""
Storage service — Supabase Storage integration for file uploads.
"""
import uuid
from typing import Optional

from supabase import create_client, Client
from fastapi import HTTPException, status, UploadFile

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class StorageService:
    def __init__(self):
        self.client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        self.bucket = settings.STORAGE_BUCKET

    def _ensure_bucket_exists(self) -> None:
        """Create the storage bucket if it doesn't exist."""
        try:
            self.client.storage.get_bucket(self.bucket)
        except Exception:
            try:
                self.client.storage.create_bucket(
                    self.bucket,
                    options={"public": False, "file_size_limit": 10485760}  # 10MB
                )
                logger.info(f"Created storage bucket: {self.bucket}")
            except Exception as e:
                logger.warning(f"Bucket creation skipped (may already exist): {e}")

    async def upload_file(self, file: UploadFile, user_id: str) -> dict:
        """Upload a file to Supabase Storage. Returns file URL and metadata."""
        self._ensure_bucket_exists()

        # Validate file type
        allowed_types = {"application/pdf", "application/msword",
                         "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF, DOC, and DOCX files are allowed"
            )

        # Read file content
        content = await file.read()
        file_size = len(content)

        # Validate file size (10MB max)
        if file_size > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must be less than 10MB"
            )

        # Generate unique path
        file_ext = file.filename.rsplit(".", 1)[-1].lower() if file.filename else "pdf"
        storage_path = f"{user_id}/{uuid.uuid4()}.{file_ext}"

        try:
            # Upload to Supabase Storage
            self.client.storage.from_(self.bucket).upload(
                path=storage_path,
                file=content,
                file_options={"content-type": file.content_type}
            )

            # Get public URL
            file_url = f"{settings.SUPABASE_URL}/storage/v1/object/{self.bucket}/{storage_path}"

            logger.info(f"File uploaded: {storage_path} ({file_size} bytes)")

            return {
                "file_url": file_url,
                "storage_path": storage_path,
                "file_size": file_size,
                "file_type": file_ext,
                "filename": file.filename or f"resume.{file_ext}",
                "content": content,
            }
        except Exception as e:
            logger.error(f"File upload failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"File upload failed: {str(e)}"
            )

    def download_file(self, storage_path: str) -> bytes:
        """Download a file from Supabase Storage."""
        try:
            response = self.client.storage.from_(self.bucket).download(storage_path)
            return response
        except Exception as e:
            logger.error(f"File download failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )

    def delete_file(self, storage_path: str) -> None:
        """Delete a file from Supabase Storage."""
        try:
            self.client.storage.from_(self.bucket).remove([storage_path])
            logger.info(f"File deleted: {storage_path}")
        except Exception as e:
            logger.warning(f"File deletion failed: {e}")

    def get_signed_url(self, storage_path: str, expires_in: int = 3600) -> str:
        """Generate a signed URL for temporary file access."""
        try:
            response = self.client.storage.from_(self.bucket).create_signed_url(
                storage_path, expires_in
            )
            return response["signedURL"]
        except Exception as e:
            logger.error(f"Signed URL generation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not generate file URL"
            )
