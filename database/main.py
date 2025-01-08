from fastapi import FastAPI, Depends
from database import Base, engine, get_db
from sqlalchemy.orm import Session

app = FastAPI(title="Time Travel ChatBot")

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to Time Travel ChatBot"}

