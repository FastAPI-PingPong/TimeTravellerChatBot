from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class UserModel(Base):
    """
    사용자 정보를 저장하는 모델

    Attributes:
        id (int): 사용자의 고유 식별자
        username (str): 사용자의 고유한 사용자명
        hashed_password (str): PBKDF2-SHA256으로 해시화된 비밀번호
        sessions (list[SessionModel]): 사용자의 대화 세션 목록

    Relationships:
        - sessions: 일대다 관계로 SessionModel과 연결됨
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    sessions = relationship("SessionModel", back_populates="user")


class SessionModel(Base):
    """
    대화 세션 정보를 저장하는 모델

    Attributes:
        id (int): 세션의 고유 식별자
        user_id (int): 세션을 소유한 사용자의 ID (Foreign Key)
        year (int): 세션의 연도 설정
        location (str): 세션의 위치 설정
        persona (str): 세션의 인물 설정
        created_at (datetime): 세션 생성 시간

    Relationships:
        - user: 다대일 관계로 UserModel과 연결됨
        - chats: 일대다 관계로 ChatModel과 연결됨
    """

    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    year = Column(Integer)
    location = Column(String)
    persona = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UserModel", back_populates="sessions")
    chats = relationship("ChatModel", back_populates="session")


class ChatModel(Base):
    """
    개별 대화 내용을 저장하는 모델

    Attributes:
        id (int): 대화의 고유 식별자
        session_id (int): 대화가 속한 세션의 ID (Foreign Key)
        question (str): 사용자의 질문 내용
        answer (str): ChatGPT의 응답 내용
        created_at (datetime): 대화 생성 시간

    Relationships:
        - session: 다대일 관계로 SessionModel과 연결됨
    """

    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    question = Column(String)
    answer = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("SessionModel", back_populates="chats")
