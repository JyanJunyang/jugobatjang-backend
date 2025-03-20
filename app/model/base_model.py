from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
