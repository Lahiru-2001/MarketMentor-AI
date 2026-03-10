from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.core.dependencies import get_db
from backend.core.security import get_current_user
from backend.api.schemas.user_profile import (
    ProfileResponse,
    ProfileUpdate
)
from backend.services.user_services.profile_service import (
    get_profile,
    update_profile
)

router = APIRouter(tags=["Profile"])


@router.get("/", response_model=ProfileResponse)
def view_profile(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    profile = get_profile(db, user_id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.put("/update")
def edit_profile(
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    success, message = update_profile(db, user_id, data)

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"message": message}