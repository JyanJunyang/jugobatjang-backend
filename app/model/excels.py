from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlmodel import Field

from app.model.base_model import BaseModel


class Excels(BaseModel, table=True):
    """엑셀 테이블"""

    __tablename__ = "excels"

    id: int = Field(primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id")
    file_name: str = Field(sa_column=Column(String(225), nullable=False))
    upload_date: datetime = Field(sa_column=Column(DateTime, nullable=False))
    share_count: int = Field(sa_column=Column(Integer, default=0))
    max_share_count: int = Field(sa_column=Column(Integer, default=10))
