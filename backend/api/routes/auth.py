from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...core.security import create_access_token
from ...db.session import SessionLocal
from ...api.schemas.user import UserRegister, UserLogin
from ...services.user_services.auth_service import register_user, login_user


router = APIRouter(tags=["Auth"])



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):

    success, message = register_user(
        db=db,
        username=data.username,
        email=data.email,
        confirm_email=data.confirm_email,
        password=data.password
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    return {"message": message}



@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    success, message, user_data = login_user(
        db,
        email=data.email,
        password=data.password
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message
        )

    if "user_id" not in user_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User ID missing in login response"
        )

    access_token = create_access_token(
        data={
            "sub": str(user_data["user_id"]),
            "user_type": user_data["user_type"]
        }
    )

    return {
        "message": message,
        "access_token": access_token,
        "user_type": user_data["user_type"]
    }
