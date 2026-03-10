from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import text
from jose import jwt, JWTError

from backend.core.security import SECRET_KEY, ALGORITHM
from backend.core.dependencies import get_db
from backend.db.crud import save_support_message
from backend.api.schemas.support import SupportCreate

router = APIRouter()


# -----------------------------
# Get Current User ID From Token
# -----------------------------
def get_current_user_id(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload.get("sub"))
    except JWTError:
        return None


# -----------------------------
# SEND SUPPORT MESSAGE
# -----------------------------
@router.post("/send")
def send_support_message(
    request: SupportCreate,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")
    user_id = get_current_user_id(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    save_support_message(db, {
        "user_id": user_id,
        "username": request.username,
        "email": request.email,
        "issue_type": request.issue_type,
        "description": request.description,
        "status": "Pending"
    })

    return {"message": "Support message sent successfully"}


# ---------------------------------------------------
# GET ALL SUPPORT MESSAGES FOR LOGGED-IN USER
# ---------------------------------------------------
@router.get("/my-messages")
def get_my_support_messages(
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")
    user_id = get_current_user_id(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Get support messages
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

    result = []

    for support in supports:
        # Get replies for each support
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

        result.append({
            "support_id": support["support_id"],
            "issue_type": support["issue_type"],
            "description": support["description"],
            "status": support["status"],
            "created_at": support["created_at"],
            "replies": replies
        })

    return result