from sqlalchemy import Column, Integer, String
from sqlmodel import Field, Relationship

from app.model.base_model import BaseModel
from app.model.users import Users


class Relationships(BaseModel, table=True):
    """관계 테이블"""

    user_id: int = Field(default=None, foreign_key="users.id")
    type_no: int = Field(sa_column=Column(Integer, nullable=False))
    name: str = Field(sa_column=Column(String(64), nullable=False))
    color_code: str = Field(sa_column=Column(String(7), nullable=False))

    users: Users = Relationship(back_populates="relationships")
