import re
from sqlalchemy.orm import Session
from backend.db.models import User
from backend.core.security import hash_password, verify_password


PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$"
)

def register_user(
    db: Session,
    username: str,
    email: str,
    confirm_email: str,
    password: str
):
   
    if db.query(User).filter(User.username == username).first():
        return False, "Username already exists. Try again."

    
    if email != confirm_email:
        return False, "Email and confirm email do not match."

    if db.query(User).filter(User.email == email).first():
        return False, "Email already exists. Try again."

   
    if not PASSWORD_REGEX.match(password):
        return False, "Password does not meet security requirements."

 
    new_user = User(
        username=username,
        email=email,
        password=hash_password(password),
        user_type="client"   
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return True, "Registration successful."



def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return False, "Invalid email or password.", None

    if not verify_password(password, user.password):
        return False, "Invalid email or password.", None

   
    return True, "Login successful.", {
        "user_id": user.user_id,              
        "user_type": user.user_type
    }
