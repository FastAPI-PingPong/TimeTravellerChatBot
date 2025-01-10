from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from .database import create_tables, get_db
from .auth import verify_password, create_token, get_user_from_access_token

from .schemas import (
    UserCreate,
    UserCreateResposne,
    TokenResponse,
    SessionCreate,
    SessionCreateResponse,
    ChatCreate,
    ChatResponse,
)
from .models import UserModel, SessionModel, ChatModel
from .chat import ChatManager
from .orm import ORM


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Database의 모든 model이 정의된 이후에 명시적으로 table을 생성
    """
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/signup", response_model=UserCreateResposne)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    orm = ORM(db)
    if orm.check_username_exists(user.username):
        raise HTTPException(status_code=409, detail="Username is already taken.")

    new_user = orm.create_user(user)
    return new_user


@app.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    orm = ORM(db)
    user = orm.get_user_by_username(form_data.username)
    if (
        not user
        or not form_data.password
        or not verify_password(form_data.password, str(user.hashed_password))
    ):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_token(str(user.username))
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/session", response_model=SessionCreateResponse)
async def create_session(
    session_create_data: SessionCreate,
    user: UserModel = Depends(get_user_from_access_token),
    db: Session = Depends(get_db),
):
    orm = ORM(db)
    new_session = orm.create_session(session_create_data, user.id)
    return new_session


@app.get("/introduction/{session_id}", response_model=ChatResponse)
async def get_introduction(
    session_id: int,
    user: UserModel = Depends(get_user_from_access_token),
    db: Session = Depends(get_db),
):
    """
    가상인물의 자기소개 멘트를 반환.
    """
    # TODO: ChatManager를 통해 첫 질문(introduction)을 받아오고 대답을 reponse로 반환
    chat_manager = ChatManager(session_id, db)
    introduction = chat_manager.get_introduction()
    return {"question": "", "answer": introduction}


@app.post("/chat/{session_id}", response_model=list[ChatResponse])
async def chat(
    session_id: int,
    chat_create_data: ChatCreate,
    user: UserModel = Depends(get_user_from_access_token),
    db: Session = Depends(get_db),
):
    chat_manager = ChatManager(session_id, db)
    answer = chat_manager.get_answer(chat_create_data.question)
    orm = ORM(db)
    chats = orm.get_chats_by_session(session_id)
    chat_list = [{"question": chat.question, "answer": chat.answer} for chat in chats]
    return chat_list
