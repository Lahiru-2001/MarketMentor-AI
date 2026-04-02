
from pydantic import BaseModel, EmailStr, Field


# SupportCreate model defines the structure of support request data
class SupportCreate(BaseModel):
    
    # Username must be a string with at least 2 characters
    username: str = Field(min_length=2)
    
    # Email must be a valid email address
    email: EmailStr
    
    # Type of issue submitted by the user (e.g., technical, billing, general)
    issue_type: str
    
    # Description must be at least 5 characters long
    description: str = Field(min_length=5)