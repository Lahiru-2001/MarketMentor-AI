from pydantic import BaseModel, EmailStr
from typing import Optional


class ProfileResponse(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    country: Optional[str]
    investment_objective: Optional[str]
    profile_image: Optional[str]

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    country: Optional[str] = None
    investment_objective: Optional[str] = None
    profile_image: Optional[str] = None