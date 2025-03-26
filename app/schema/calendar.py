from datetime import datetime

from pydantic import BaseModel, Field


class CreateCalendarDTOModel(BaseModel):
    """캘린더 일정 생성할 때 필요한 요청 DTO"""

    title: str = Field(..., description="일정 제목")
    date: datetime = Field(..., description="캘린더 일정 - Record.event_date와 같음")
    user_id: int = Field(..., description="유저 ID")
    record_id: int | None = Field(default=None, description="기록 ID")
    event_type_id: int | None = Field(default=None, description="이벤트 ID")
    relation_id: int | None = Field(default=None, description="관계 ID")
