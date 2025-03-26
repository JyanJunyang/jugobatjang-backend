from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Integer, SmallInteger, String
from sqlmodel import Field

from app.model.base_model import BaseModel


class StatusEnum(str, Enum):
    A = "A"
    N = "N"
    U = "U"


class EventTypes(BaseModel, table=True):
    """경조사 타입 테이블."""

    __tablename__ = "eventtypes"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(48), nullable=False))
    user_id: int = Field(sa_column=Column(Integer, nullable=True))
    color_code: str = Field(sa_column=Column(String(7), nullable=False))
    type_no: int = Field(sa_column=Column(Integer, nullable=False))


class Relations(BaseModel, table=True):
    """관계 테이블"""

    __tablename__ = "relations"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(48), nullable=False))
    user_id: int = Field(sa_column=Column(Integer, nullable=True))
    color_code: str = Field(sa_column=Column(String(7), nullable=False))
    type_no: int = Field(sa_column=Column(Integer, nullable=False))


class Records(BaseModel, table=True):
    """기록 테이블"""

    __tablename__ = "records"

    id: int = Field(default=None, primary_key=True)
    event_type_id: int = Field(sa_column=Column(Integer, nullable=False))
    relation_id: int = Field(sa_column=Column(Integer, nullable=False))
    user_id: int = Field(sa_column=Column(Integer, nullable=False))
    is_received: int = Field(sa_column=Column(SmallInteger, nullable=False))
    date: datetime = Field(
        sa_column=Column(DateTime, nullable=False, comment="금액을 주거나 받은 날짜")
    )
    peer_name: str = Field(
        sa_column=Column(
            String(64), nullable=True, comment="금액을 주거나 받은 상대방의 이름"
        )
    )
    calendar_date: datetime = Field(
        sa_column=Column(DateTime, nullable=True, comment="캘린더 일정")
    )
    peer_name: str = Field(sa_column=Column(String(40), nullable=True))
    excel_id: int = Field(sa_column=Column(Integer, nullable=True))
    phone: str = Field(sa_column=Column(String(64), nullable=True))
    amount: int = Field(sa_column=Column(Integer, default=0))
    status: StatusEnum = Field(sa_column=Column(String(4), default="A"))
    memo: str = Field(sa_column=Column(String(225), nullable=True))
