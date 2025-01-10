from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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
from .models import UserModel
from .chat import ChatManager
from .orm import ORM


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    애플리케이션 시작 시 데이터베이스 테이블을 생성하는 lifespan 이벤트 핸들러
    """
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return FileResponse("static/login.html")


@app.post("/signup", response_model=UserCreateResposne)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    새로운 사용자를 등록하는 엔드포인트

    Args: 사용자 생성 정보
    - username: 사용자명
    - password: 비밀번호

    Returns: 생성된 사용자 정보
    - id: 사용자 ID
    - username: 사용자명

    Raises:
        409: 사용자명이 이미 존재하는 경우
    """
    orm = ORM(db)
    if orm.check_username_exists(user.username):
        raise HTTPException(status_code=409, detail="Username is already taken.")

    new_user = orm.create_user(user)
    return new_user


@app.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    사용자 로그인을 처리하는 엔드포인트

    Args: 로그인 폼 데이터
    - username: 사용자명
    - password: 비밀번호

    Returns: 토큰 정보
    - access_token: JWT 액세스 토큰
    - token_type: 토큰 타입 (bearer)

    Raises:
        401: 잘못된 사용자명이나 비밀번호
    """
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
    """
    ChatGPT와의 새로운 채팅 세션을 생성하는 엔드포인트

    Args: 세션 생성 정보
    - year: 가상인물의 시대 연도
    - location: 가상인물의 위치 정보
    - persona: 가상인물의 페르소나 정보

    Returns: 생성된 세션 정보
    - id: 세션 ID
    """
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
    특정 세션에 해당되는 가상인물의 자기소개 문구를 가져오는 엔드포인트

    Args: 세션 ID
    - session_id: 세션 ID (path parameter)

    Returns: 자기소개 응답
    - question: 빈 문자열
    - answer: 가상인물의 자기소개 문구
    """
    chat_manager = ChatManager(session_id, db)
    introduction_prompt, introduction = chat_manager.get_introduction()
    orm = ORM(db)
    orm.create_chat(session_id, introduction_prompt, introduction)
    return {"question": "", "answer": introduction}


@app.post("/chat/{session_id}", response_model=list[ChatResponse])
async def chat(
    session_id: int,
    chat_create_data: ChatCreate,
    user: UserModel = Depends(get_user_from_access_token),
    db: Session = Depends(get_db),
):
    """
    ChatGPT에 새로운 질문 메시지를 전송하고 모든 질문과 답변의 기록을 반환하는 엔드포인트

    Args: 세션 ID와 새로운 질문
    - session_id: 세션 ID (path parameter)
    - question: 사용자의 질문 메시지

    Returns:
        채팅 기록 목록 (질문과 답변 쌍의 리스트)
            - question: 사용자 질문 메시지
            - answer: 가상인물의 답변 메시지
    """
    chat_manager = ChatManager(session_id, db)
    question, answer = chat_manager.get_answer(chat_create_data.question)
    orm = ORM(db)
    orm.create_chat(session_id, question, answer)
    chats = orm.get_chats_by_session(session_id)
    chat_list = [{"question": chat.question, "answer": chat.answer} for chat in chats]
    return chat_list
