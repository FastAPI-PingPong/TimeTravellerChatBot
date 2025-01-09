from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from .database import create_tables, get_db
from .auth import get_hashed_password
from .schemas import UserCreate, UserCreateResposne
from .models import User


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
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=409, detail="Username is already taken.")
    hashed_password = get_hashed_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
