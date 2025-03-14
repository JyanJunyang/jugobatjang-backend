from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlmodel import Column, Field, Relationship

from app.model.base_model import BaseModel


class LoginTypeEnum(str, Enum):
    """로그인 타입 enum"""

    KAKAO = "KAKAO"
    EMAIL = "EMAIL"


class GenderEnum(str, Enum):
    """성별 enum"""

    F = "F"
    M = "M"


class Users(BaseModel, table=True):
    """유저 테이블"""

    __tablename__ = "users"

    id: int = Field(primary_key=True)
    email: str = Field(sa_column=Column(String(128), unique=True, nullable=False))
    password: str = Field(sa_column=Column(String(64), nullable=True))
    login_type: LoginTypeEnum = Field(sa_column=Column(String(64), nullable=False))
    social_id: str = Field(sa_column=Column(String(64), nullable=True))
    phone: str = Field(sa_column=Column(String(64), nullable=True))
    name: str = Field(sa_column=Column(String(48), nullable=True))
    birthday: datetime = Field(sa_column=Column(DateTime, nullable=True))
    gender: GenderEnum = Field(sa_column=Column(String(2), nullable=True))
    is_married: int = Field(sa_column=Column(Integer, nullable=True))
