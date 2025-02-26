from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlmodel import Field, Relationship

from app.model.base_model import BaseModel
from app.model.event_types import EventTypes
from app.model.excels import Excels
from app.model.relationships import Relationships
from app.model.users import Users


class Event(BaseModel, table=True):
    """경조사 기록 테이블"""

    excel_id: int = Field(default=None, foreign_key="excels.id")
    event_type_id: int = Field(default=None, foreign_key="excels.id")
    relationship_id: int = Field(default=None, foreign_key="excels.id")
    event_date: datetime = Field(sa_column=Column(DateTime, nullable=False))
    name: str = Field(sa_column=Column(String(64), nullable=False))
    phone: str = Field(sa_column=Column(String(64), nullable=False))
    amount: int = Field(sa_column=Column(Integer, default=0))
    status: str = Field(sa_column=Column(String(2), nullable=False, default="A"))
    memo: str = Field(sa_column=Column(String(225), nullable=True))

    excels: Excels = Relationship(back_populates="events")
    event_types: EventTypes = Relationship(back_populates="event_types")
    relationships: Relationships = Relationship(back_populates="relationships")
