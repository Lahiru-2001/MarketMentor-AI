import re
from sqlalchemy.orm import Session
from backend.db.models import User
from backend.core.security import hash_password, verify_password

# Regular expression for password validation:
# At least 8 characters, one lowercase letter, one uppercase letter,
# one digit, and one special character
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
    
    # Check whether the username already exists in the database
    if db.query(User).filter(User.username == username).first():
        return False, "Username already exists. Try again."

    # Check if email and confirm email match
    if email != confirm_email:
        return False, "Email and confirm email do not match."

    # Check whether the email is already registered
    if db.query(User).filter(User.email == email).first():
        return False, "Email already exists. Try again."

    # Validate password against security rules
    if not PASSWORD_REGEX.match(password):
        return False, "Password does not meet security requirements."

    # Create a new user object with hashed password
    new_user = User(
        username=username,
        email=email,
        password=hash_password(password),   # Store encrypted password
        user_type="client"                  # Default role assigned
    )

    # Save new user into database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return True, "Registration successful."


def login_user(db: Session, email: str, password: str):
    
    # Search user by email
    user = db.query(User).filter(User.email == email).first()

    # Return error if user is not found
    if not user:
        return False, "Invalid email or password.", None

    # Verify entered password against stored hashed password
    if not verify_password(password, user.password):
        return False, "Invalid email or password.", None

    # Login successful: return user details
    return True, "Login successful.", {
        "user_id": user.user_id,     # Unique user ID
        "user_type": user.user_type  # User role (client/admin/etc.)
    }