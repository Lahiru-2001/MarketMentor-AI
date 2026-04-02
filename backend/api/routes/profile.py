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

# Create API router and assign tag for Swagger documentation grouping
router = APIRouter(tags=["Profile"])

# VIEW USER PROFILE ENDPOINT
@router.get("/", response_model=ProfileResponse)
def view_profile(
    db: Session = Depends(get_db),              
    user_id: int = Depends(get_current_user)    
):
    # Retrieve profile data from service layer
    profile = get_profile(db, user_id)

    # If profile does not exist, return 404 error
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Return profile data
    return profile

# UPDATE USER PROFILE ENDPOINT
@router.put("/update")
def edit_profile(
    data: ProfileUpdate,                        
    db: Session = Depends(get_db),          
    user_id: int = Depends(get_current_user)    
):
    # Call service layer to update profile
    success, message = update_profile(db, user_id, data)

    # If update fails, return 400 error with message
    if not success:
        raise HTTPException(status_code=400, detail=message)

    # Return success message
    return {"message": message}