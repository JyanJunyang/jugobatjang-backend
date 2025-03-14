from sqlalchemy import Column, Integer, String
from sqlmodel import Field

from app.model.base_model import BaseModel


class Relationships(BaseModel, table=True):
    """관계 테이블"""

    __tablename__ = "relationships"

    id: int = Field(primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id")
    type_no: int = Field(sa_column=Column(Integer, nullable=False))
    name: str = Field(sa_column=Column(String(64), nullable=False))
    color_code: str = Field(sa_column=Column(String(7), nullable=False))


class RelationDetails(BaseModel, table=True):
    """추후 관계 테이블의 자식 테이블"""

    __tablename__ = "relation_details"
