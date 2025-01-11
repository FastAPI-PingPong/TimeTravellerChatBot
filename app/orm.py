from sqlalchemy.orm import Session
from .models import UserModel, SessionModel, ChatModel
from .schemas import UserCreate, SessionCreate
from .auth import get_hashed_password


class ORM:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> UserModel | None:
        """사용자 이름으로 유저 조회"""
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    def check_username_exists(self, username: str) -> bool:
        """사용자 이름 존재 여부 확인"""
        return self.get_user_by_username(username) is not None

    def create_user(self, user: UserCreate) -> UserModel:
        """새로운 유저 생성"""
        hashed_password = get_hashed_password(user.password)
        new_user = UserModel(username=user.username, hashed_password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def create_session(self, session_data: SessionCreate, user_id: int) -> SessionModel:
        """새로운 세션 생성"""
        new_session = SessionModel(user_id=user_id, **session_data.model_dump())
        self.db.add(new_session)
        self.db.commit()
        self.db.refresh(new_session)
        return new_session

    def get_session_by_id(self, session_id: int) -> SessionModel | None:
        """세션 ID로 세션 조회"""
        return self.db.query(SessionModel).filter(SessionModel.id == session_id).first()

    def get_sessions_by_user(
        self, user_id: int, get_recent: bool = True, recent_count: int = 5
    ) -> list[SessionModel]:
        """사용자 ID로 세션 조회"""
        sessions_for_user_id = self.db.query(SessionModel).filter(
            SessionModel.user_id == user_id
        )
        if not get_recent:
            return sessions_for_user_id.all()
        return (
            sessions_for_user_id.order_by(SessionModel.created_at.desc())
            .limit(recent_count)
            .all()
        )

    def create_chat(self, session_id: int, question: str, answer: str) -> ChatModel:
        """새로운 채팅 생성"""
        new_chat = ChatModel(session_id=session_id, question=question, answer=answer)
        self.db.add(new_chat)
        self.db.commit()
        self.db.refresh(new_chat)
        return new_chat

    def get_chats_by_session(self, session_id: int) -> list[ChatModel]:
        """세션 ID로 채팅 내역 조회"""
        return self.db.query(ChatModel).filter(ChatModel.session_id == session_id).all()
