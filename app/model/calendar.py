from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlmodel import Field

from app.model.base_model import BaseModel


class Calendar(BaseModel, table=True):
    """캘린더 테이블."""

    __tablename__ = "calendar"

    id: int = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(String(64), nullable=False))
    date: datetime = Field(
        sa_column=Column(DateTime, nullable=False, comment="금액을 주거나 받은 날짜")
    )
    user_id: int = Field(sa_column=Column(Integer, nullable=False))
    record_id: int = Field(sa_column=Column(Integer, nullable=True))
    event_type_id: int = Field(sa_column=Column(Integer, nullable=True))
    relation_id: int = Field(sa_column=Column(Integer, nullable=True))
