from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from .base import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    user_type = Column(String(20), default="Client")
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(String(20), default="Active")
