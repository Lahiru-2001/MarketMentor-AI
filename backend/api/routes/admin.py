from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.core.dependencies import get_db
from backend.core.security import get_current_user
from backend.db.models import User

router = APIRouter(tags=["Admin"])


# -----------------------------
# GET ALL USERS (JOIN PROFILE)
# -----------------------------
@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    # Check if admin
    admin = db.query(User).filter(User.user_id == current_user).first()

    if not admin or admin.user_type != "Admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    # Fetch users with user_type 'Client' or 'client' only
    query = text("""
        SELECT 
            u.user_id,
            u.username,
            u.email,
            u.status,
            up.first_name,
            up.last_name,
            up.phone_number,
            up.country,
            up.investment_objective
        FROM users u
        LEFT JOIN user_profile up
            ON u.user_id = up.user_id
        WHERE LOWER(u.user_type) = 'client'  -- Case-insensitive check for 'Client' or 'client'
        ORDER BY u.user_id DESC
    """)

    result = db.execute(query).mappings().all()
    return result

# -----------------------------
# DEACTIVATE USER
# -----------------------------
@router.put("/deactivate/{user_id}")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    admin = db.query(User).filter(User.user_id == current_user).first()

    if not admin or admin.user_type != "Admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.status = "Inactive"
    db.commit()

    return {"message": "User deactivated successfully"}

# -----------------------------
# GET ALL SUPPORT MESSAGES
# -----------------------------
@router.get("/support")
def get_all_support(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    admin = db.query(User).filter(User.user_id == current_user).first()

    if not admin or admin.user_type != "Admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    query = text("""
        SELECT 
            s.support_id,
            s.username,
            s.email,
            s.issue_type,
            s.description,
            s.created_at,
            s.status
        FROM support s
        ORDER BY s.support_id DESC
    """)

    result = db.execute(query).mappings().all()
    return result


# -----------------------------
# REPLY TO SUPPORT MESSAGE
# -----------------------------
@router.post("/support/reply/{support_id}")
def reply_support_message(
    support_id: int,
    reply_data: dict,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    admin = db.query(User).filter(User.user_id == current_user).first()

    if not admin or admin.user_type != "Admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    # Check support exists
    support = db.execute(
        text("SELECT * FROM support WHERE support_id = :id"),
        {"id": support_id}
    ).fetchone()

    if not support:
        raise HTTPException(status_code=404, detail="Support message not found")

    # Insert reply
    db.execute(
        text("""
            INSERT INTO reply_support (support_id, admin_id, reply_message)
            VALUES (:support_id, :admin_id, :reply_message)
        """),
        {
            "support_id": support_id,
            "admin_id": current_user,
            "reply_message": reply_data.get("reply_message")
        }
    )

    # Update support status
    db.execute(
        text("""
            UPDATE support
            SET status = 'Replied'
            WHERE support_id = :support_id
        """),
        {"support_id": support_id}
    )

    db.commit()

    return {"message": "Reply sent successfully"}

# ---------------------------------------
# GET REPLIES BY SUPPORT ID
# ---------------------------------------
@router.get("/support/replies/{support_id}")
def get_support_replies(
    support_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    admin = db.query(User).filter(User.user_id == current_user).first()

    if not admin or admin.user_type != "Admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    replies = db.execute(
        text("""
            SELECT 
                r.reply_id,
                r.reply_message,
                r.created_at,
                u.username AS admin_name
            FROM reply_support r
            JOIN users u ON r.admin_id = u.user_id
            WHERE r.support_id = :support_id
            ORDER BY r.reply_id DESC
        """),
        {"support_id": support_id}
    ).mappings().all()

    return replies