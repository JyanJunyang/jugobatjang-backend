from enum import Enum

from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship

from app.model.base_model import BaseModel
from app.model.users import Users


class EventTypes(BaseModel, table=True):
    """경조사 종류 테이블"""

    __tablename__ = "event_types"

    user_id: int = Field(default=None, foreign_key="users.id")
    type_no: int = Field(
        sa_column=Column(Integer, nullable=False)
    )  # enum으로 빼는 게 더 이상한 거 같음...
    name: str = Field(sa_column=Column(String(64), nullable=False))
    color_code: str = Field(sa_column=Column(String(7), nullable=False))

    users: Users = Relationship(back_populates="event_types")
