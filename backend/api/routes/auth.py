from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.security import create_access_token
from db.session import SessionLocal
from api.schemas.user import UserRegister, UserLogin
from services.user_services.auth_service import register_user, login_user


# Create API router and group routes under "Auth" tag
router = APIRouter(tags=["Auth"])


# Dependency function to create and close database session automatically
def get_db():
    db = SessionLocal()   
    try:
        yield db          
    finally:
        db.close()        

# USER REGISTRATION ROUTE
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.
    Accepts validated user input and calls register service.
    """

    # Call service layer function to register user
    success, message = register_user(
        db=db,
        username=data.username,
        email=data.email,
        confirm_email=data.confirm_email,
        password=data.password
    )

    # If registration fails, return HTTP 400 error
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    # Return success response
    return {"message": message}


# USER LOGIN ROUTE
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and generate JWT token.
    """

    # Call service layer function to validate login credentials
    success, message, user_data = login_user(
        db,
        email=data.email,
        password=data.password
    )

    # If login fails, return HTTP 401 Unauthorized
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message
        )

    # Ensure user_id exists before creating token
    if "user_id" not in user_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User ID missing in login response"
        )

    # Create JWT access token using user ID and user type
    access_token = create_access_token(
        data={
            "sub": str(user_data["user_id"]),   # subject = user id
            "user_type": user_data["user_type"] # role info
        }
    )

    # Return login response with token
    return {
        "message": message,
        "access_token": access_token,
        "user_type": user_data["user_type"]
    }