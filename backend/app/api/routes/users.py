"""
User profile routes.
"""
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdateRequest, PasswordChangeRequest
from app.schemas.auth import MessageResponse
from app.repositories.user_repo import UserRepository
from app.core.security import verify_password, hash_password
from app.services.storage_service import StorageService
from fastapi import HTTPException, status

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get the current user's profile."""
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_profile(
    data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update user profile fields."""
    repo = UserRepository(db)

    if data.full_name is not None:
        current_user.full_name = data.full_name
    if data.avatar_url is not None:
        current_user.avatar_url = data.avatar_url
    if data.preferences is not None:
        current_user.preferences = data.preferences

    return repo.update(current_user)


@router.post("/me/avatar", response_model=UserResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload a profile avatar."""
    # Validate image type
    allowed = {"image/jpeg", "image/png", "image/webp", "image/gif"}
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, WebP, and GIF images are allowed")

    storage = StorageService()
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Avatar must be less than 5MB")

    # Upload to Supabase Storage
    import uuid
    ext = file.filename.rsplit(".", 1)[-1] if file.filename else "jpg"
    path = f"avatars/{current_user.id}/{uuid.uuid4()}.{ext}"

    try:
        storage.client.storage.from_(storage.bucket).upload(
            path=path, file=content,
            file_options={"content-type": file.content_type}
        )
        avatar_url = f"{storage.client.supabase_url}/storage/v1/object/public/{storage.bucket}/{path}"
        current_user.avatar_url = avatar_url
        repo = UserRepository(db)
        return repo.update(current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Avatar upload failed: {str(e)}")


@router.post("/me/change-password", response_model=MessageResponse)
def change_password(
    data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change user password."""
    if not verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    repo = UserRepository(db)
    current_user.hashed_password = hash_password(data.new_password)
    repo.update(current_user)
    return MessageResponse(message="Password changed successfully")


@router.delete("/me", response_model=MessageResponse)
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete user account and all associated data."""
    repo = UserRepository(db)
    repo.delete(current_user)
    return MessageResponse(message="Account deleted successfully")
