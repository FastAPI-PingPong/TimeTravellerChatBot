from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./time_traveller.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_tables():
    """
    데이터베이스의 모든 테이블을 생성

    애플리케이션 시작 시 한 번 호출되어야 함.
    모든 SQLAlchemy 모델에 대한 테이블을 생성함.
    이미 테이블이 존재하는 경우 아무 작업도 수행하지 않음.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    데이터베이스 세션을 생성하고 관리하는 의존성 주입 함수

    FastAPI의 의존성 주입 시스템에서 사용되며,
    요청마다 새로운 데이터베이스 세션을 생성하고
    요청 처리가 완료되면 세션을 자동으로 닫음.

    Yields:
        Session: SQLAlchemy 데이터베이스 세션 객체

    Notes:
        - 이 함수는 컨텍스트 관리자로 동작하여 예외가 발생하더라도 세션이 항상 닫히는 것을 보장함.
        - FastAPI의 Depends를 통해 라우터에서 주입하여 사용함.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
