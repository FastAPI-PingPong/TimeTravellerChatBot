from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from .database import create_tables, get_db
from .auth import (
    get_hashed_password,
    verify_password,
    create_token,
)
from .schemas import UserCreate, UserCreateResposne, TokenResponse
from .models import UserModel


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
    if db.query(UserModel).filter(UserModel.username == user.username).first():
        raise HTTPException(status_code=409, detail="Username is already taken.")
    hashed_password = get_hashed_password(user.password)
    new_user = UserModel(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if (
        not user
        or not form_data.password
        or not verify_password(form_data.password, str(user.hashed_password))
    ):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_token(str(user.username))
    return {"access_token": access_token, "token_type": "bearer"}
