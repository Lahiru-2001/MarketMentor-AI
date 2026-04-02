from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import text
from jose import jwt, JWTError
from backend.core.security import SECRET_KEY, ALGORITHM
from backend.core.dependencies import get_db
from backend.db.crud import save_support_message
from backend.api.schemas.support import SupportCreate

router = APIRouter()


# FUNCTION: Extract current logged-in user ID from JWT token
def get_current_user_id(token: str):
    """
    Decode JWT token and extract user ID from payload.

    Parameters:
        token (str): JWT token sent in Authorization header

    Returns:
        int | None: User ID if token is valid, otherwise None
    """
    try:
        # Decode JWT token using secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract user ID stored in 'sub' field
        return int(payload.get("sub"))

    except JWTError:
        # Return None if token is invalid or expired
        return None


# API: Send support message
@router.post("/send")
def send_support_message(
    request: SupportCreate,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """
    Allow logged-in user to send a support message.

    Steps:
    1. Validate authorization token
    2. Extract user ID from token
    3. Save support message in database
    """

    # Check if Authorization header exists
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    # Remove 'Bearer ' prefix from token
    token = authorization.replace("Bearer ", "")

    # Get current user ID from token
    user_id = get_current_user_id(token)

    # If token invalid → unauthorized access
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Save support message into database
    save_support_message(db, {
        "user_id": user_id,
        "username": request.username,
        "email": request.email,
        "issue_type": request.issue_type,
        "description": request.description,
        "status": "Pending"   # Default status when message is first created
    })

    # Success response
    return {"message": "Support message sent successfully"}


# API: Get all support messages of logged-in user
@router.get("/my-messages")
def get_my_support_messages(
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """
    Retrieve all support messages submitted by logged-in user.

    Also fetch admin replies related to each support message.
    """

    # Check token exists
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    # Extract token from Authorization header
    token = authorization.replace("Bearer ", "")

    # Decode token and get user ID
    user_id = get_current_user_id(token)

    # If token invalid
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Fetch all support messages belonging to current user
    supports = db.execute(
        text("""
            SELECT 
                support_id,
                issue_type,
                description,
                status,
                created_at
            FROM support
            WHERE user_id = :user_id
            ORDER BY support_id DESC
        """),
        {"user_id": user_id}
    ).mappings().all()

    # Store final response list
    result = []



    # Fetch replies linked to that support message
    for support in supports:

        replies = db.execute(
            text("""
                SELECT 
                    r.reply_message,
                    r.created_at,
                    u.username AS admin_name
                FROM reply_support r
                JOIN users u ON r.admin_id = u.user_id
                WHERE r.support_id = :support_id
                ORDER BY r.reply_id ASC
            """),
            {"support_id": support["support_id"]}
        ).mappings().all()

        # Append support message + replies
        result.append({
            "support_id": support["support_id"],
            "issue_type": support["issue_type"],
            "description": support["description"],
            "status": support["status"],
            "created_at": support["created_at"],
            "replies": replies
        })

    # Return all support messages with replies
    return result