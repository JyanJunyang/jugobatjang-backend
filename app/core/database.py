from contextlib import contextmanager
from typing import Generator, List, Type, TypeVar

import pymysql
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import configs

engine = create_engine(configs.DATABASE_URI, echo=True)

SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


T = TypeVar("T", bound=BaseModel)


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


def convert_rows_to_dict_list(query_result, dto_class: Type[T]) -> List[T]:
    """SQLAlchemy Rowresult -> Dict List 형태로 형변환 해주는 메소드."""
    return [dto_class(**dict(row._mapping)) for row in query_result]


def convert_page_to_offset(size: int, page: int):
    """파라미터로 받은 paging 파라미터, offset 값으로 변환"""
    return (page - 1) * size
