from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from backend.core.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt


# Create password hashing context using bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash plain password before storing in database
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Verify entered password against stored hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Load JWT secret key from configuration
SECRET_KEY = settings.SECRET_KEY

# Load encryption algorithm from configuration
ALGORITHM = settings.ALGORITHM

# Token expiration time (60 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Create JWT access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    
    # Copy input data to avoid modifying original dictionary
    to_encode = data.copy()

    # Set token expiration time
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Add expiration time into payload
    to_encode.update({"exp": expire})

    # Encode JWT token using secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# Initialize HTTP Bearer authentication
security = HTTPBearer()


# Extract and validate current user from JWT token
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
       
        # Decode JWT token
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        # Extract user ID from token payload
        user_id: str | None = payload.get("sub")

        # If no user ID found, token is invalid
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )

        # Return user ID as integer
        return int(user_id)

    except JWTError:
        # Handle invalid/expired token errors
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )