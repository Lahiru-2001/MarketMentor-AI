from sqlalchemy.orm import Session
from backend.db.models import User, UserProfile


def get_profile(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        return None

    profile = db.query(UserProfile).filter(
        UserProfile.user_id == user_id
    ).first()

    return {
        "username": user.username,
        "email": user.email,
        "first_name": profile.first_name if profile else None,
        "last_name": profile.last_name if profile else None,
        "phone_number": profile.phone_number if profile else None,
        "country": profile.country if profile else None,
        "investment_objective": profile.investment_objective if profile else None,
        "profile_image": profile.profile_image if profile else None
    }


def update_profile(db: Session, user_id: int, data):
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        return False, "User not found"

   
    existing_email = db.query(User).filter(
        User.email == data.email,
        User.user_id != user_id
    ).first()

    if existing_email:
        return False, "Email already exists"

   
    user.username = data.username
    user.email = data.email

    
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == user_id
    ).first()

    if not profile:
        profile = UserProfile(user_id=user_id)
        db.add(profile)

    profile.first_name = data.first_name
    profile.last_name = data.last_name
    profile.phone_number = data.phone_number
    profile.country = data.country
    profile.investment_objective = data.investment_objective
    profile.profile_image = data.profile_image

    db.commit()

    return True, "Profile updated successfully"