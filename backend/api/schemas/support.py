from pydantic import BaseModel, EmailStr, Field

class SupportCreate(BaseModel):
    username: str = Field(min_length=2)
    email: EmailStr
    issue_type: str
    description: str = Field(min_length=5)