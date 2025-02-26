from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import configs

engine = create_engine(configs.DATABASE_URI, echo=True)

SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)

import pymysql


@contextmanager
def start_session():
    """MySQL 연결 및 session 관리"""
    session = None
    try:
        session = SessionLocal()
        yield session
    except Exception as e:
        print(f"에러 : {str(e)}")
        raise e
    finally:
        if session:
            session.close()


def get_db() -> Generator:
    """API 호출시 발동될 메소드"""
    with start_session() as session:
        yield session
