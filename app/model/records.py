from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Integer, String
from sqlmodel import Field

from app.model.base_model import BaseModel


class EventTypes(BaseModel, table=True):
    """경조사 타입 테이블."""

    __tablename__ = "event_types"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(48), nullable=False))
    user_id: int = Field(sa_column=Column(Integer, nullable=True))
    color_code: str = Field(sa_column=Column(String(7), nullable=False))
    type_no: int = Field(sa_column=Column(Integer, nullable=False))


class Relationships(BaseModel, table=True):
    """관계 테이블"""

    __tablename__ = "relationships"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(48), nullable=False))
    user_id: int = Field(sa_column=Column(Integer, nullable=True))
    color_code: str = Field(sa_column=Column(String(7), nullable=False))
    type_no: int = Field(sa_column=Column(Integer, nullable=False))


class Records(BaseModel, table=True):
    """기록 테이블"""

    __tablename__ = "records"

    id: int = Field(default=None, primary_key=True)
    excel_id: int = Field(sa_column=Column(Integer, nullable=True))
    event_type_id: int = Field(sa_column=Column(Integer, nullable=False))
    relationship_id: int = Field(sa_column=Column(Integer, nullable=False))
    user_id: int = Field(sa_column=Column(Integer, nullable=False))
    event_date: datetime = Field(sa_column=Column(DateTime, nullable=False))
    name: str = Field(sa_column=Column(String(64), nullable=False))
    phone: str = Field(sa_column=Column(String(64), nullable=False))
    amount: int = Field(sa_column=Column(Integer, default=0))
    status: str = Field(sa_column=Column(Enum("A", "N", "U"), default="A"))
    memo: str = Field(sa_column=Column(String(225), nullable=True))
