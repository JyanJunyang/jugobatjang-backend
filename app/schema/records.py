from datetime import datetime

from pydantic import BaseModel, Field


class CreateRecordDTOModel(BaseModel):
    """경조사 장부 생성할 때 필요한 요청 DTO"""

    event_type_id: int = Field(..., description="경조사 ID")
    relation_id: int = Field(..., description="관계 ID")
    is_received: int = Field(..., description="받은내역 : 1, 준 내역 : 0")
    event_date: datetime = Field(..., description="경조사 일정")
    name: str = Field(..., description="이벤트 이름")
    amount: int = Field(..., description="금액")
    status: str = Field(default="A", description="참여 여부")
    excel_id: int | None = Field(None, description="Excel ID")
    memo: str | None = Field(None, description="메모")
    phone: str | None = Field(None, description="핸드폰 번호")
