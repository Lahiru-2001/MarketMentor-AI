from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship

from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
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

    profile = relationship("UserProfile", back_populates="user", uselist=False)

class Support(Base):
    __tablename__ = "support"

    support_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    issue_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(20), default="Pending")
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    

class UserProfile(Base):
    __tablename__ = "user_profile"

    profile_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))

    first_name = Column(String(100))
    last_name = Column(String(100))
    phone_number = Column(String(20))
    country = Column(String(100))
    investment_objective = Column(String(255))
    profile_image = Column(String(255))

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )

    status = Column(String(20), default="Active")

    user = relationship("User", back_populates="profile")



class ReplySupport(Base):
    __tablename__ = "reply_support"

    reply_id = Column(Integer, primary_key=True, index=True)
    support_id = Column(Integer, ForeignKey("support.support_id", ondelete="CASCADE"))
    admin_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    reply_message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))