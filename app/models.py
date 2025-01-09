from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    sessions = relationship("SessionModel", back_populates="user")


class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    year = Column(Integer)
    location = Column(String)
    persona = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UserModel", back_populates="sessions")


class ChatModel(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    question = Column(String)
    answer = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("SessionModel", back_populates="chats")
