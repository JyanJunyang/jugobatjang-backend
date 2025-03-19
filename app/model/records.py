from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.model.base_model import BaseModel


class EventTypes(BaseModel, table=True):
    """경조사 타입 테이블."""

    __tablename__ = "event_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    color_code = Column(String(7), nullable=False)
    type_no = Column(
        Integer, nullable=False, description="100번대 숫자부터 커스텀 경조사타입"
    )


class Relationships(BaseModel, table=True):
    """관계 테이블"""

    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(48), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    color_code = Column(String(7), nullable=False)
    type_no = Column(
        Integer, nullable=False, description="100번대 숫자부터 커스텀 관계타입"
    )


class Records(BaseModel, table=True):
    """기록 테이블"""

    __tablename__ = "records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    excel_id = Column(Integer, ForeignKey("excels.id"), nullable=True)
    event_type_id = Column(Integer, ForeignKey("event_types.id"), nullable=False)
    relationship_id = Column(Integer, ForeignKey("relationships.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    event_date = Column(DateTime, nullable=False)
    name = Column(String(64), nullable=False)
    phone = Column(String(64), nullable=False)
    amount = Column(Integer, default=0)
    status = Column(
        Enum("A", "N", "U"),
        default="A",
        description="A : 참석 ( Attend ), B : 미참석 ( No-Show), U : 미정 ( Undecided )",
    )
    memo = Column(String(225), nullable=True)
