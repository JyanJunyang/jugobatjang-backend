from datetime import datetime

from pydantic import BaseModel, Field


class CreateRecordDTOModel(BaseModel):
    """경조사 장부 생성할 때 필요한 요청 DTO"""

    event_type_id: int = Field(..., description="경조사 ID")
    relation_id: int = Field(..., description="관계 ID")
    is_received: int = Field(..., description="받은내역 : 1, 준 내역 : 0")
    date: datetime = Field(..., description="금액을 주거나 받은 날짜")
    peer_name: str = Field(..., description="금액을 주거나 받은 상대방의 이름")
    calendar_date: datetime | None = Field(default=None, description="경조사 일정")
    amount: int = Field(..., description="금액")
    status: str = Field(default="A", description="참여 여부")
    excel_id: int | None = Field(None, description="Excel ID")
    memo: str | None = Field(None, description="메모")
    phone: str | None = Field(None, description="핸드폰 번호")


class RecordSearchResponseDTOModel(BaseModel):
    """경조사 장부 조회 Response DTO"""

    id: int = Field(..., description="기록 ID")
    amount: int = Field(..., description="금액")
    is_received: int = Field(..., description="받은내역 : 1, 준 내역 : 0")
    date: datetime = Field(..., description="금액을 주거나 받은 날짜")
    peer_name: str = Field(..., description="금액을 주거나 받은 상대방의 이름")
    event_type_name: str = Field(..., description="경조사 종류 이름")
    event_color_code: str = Field(..., description="경조사 커스텀 색상")
    relation_name: str = Field(..., description="관계 이름")
    relation_color_code: str = Field(..., description="관계 커스텀 색상")


class RecordDetailDTOModel(BaseModel):
    id: int = Field(..., description="기록 ID")
    amount: int = Field(..., description="금액")
    is_received: int = Field(..., description="받은내역 : 1, 준 내역 : 0")
    phone: str | None = Field(default=None, description="대상자의 핸드폰 번호")
    status: str | None = Field(default=None, description="참여 여부 ")
    memo: str | None = Field(default=None, description="메모")
    date: datetime = Field(..., description="금액을 주거나 받은 날짜")
    peer_name: str = Field(..., description="금액을 주거나 받은 상대방의 이름")
    calendar_date: datetime = Field(..., description="경조사 일정")
    event_type_id: int = Field(..., description="경조사 ID")
    event_type_name: str = Field(..., description="경조사 종류 이름")
    event_type_color_code: str = Field(..., description="경조사 커스텀 색상")
    relation_id: int = Field(..., description="관계 ID")
    relation_name: str = Field(..., description="관계 이름")
    relation_color_code: str = Field(..., description="관계 커스텀 색상")


class EditRecordModel(BaseModel):
    """실제 업데이트 되는 기록 모델."""

    amount: int | None = Field(default=None, description="금액")
    is_received: int | None = Field(
        default=None, description="받은내역 : 1, 준 내역 : 0"
    )
    phone: str | None = Field(default=None, description="대상자의 핸드폰 번호")
    status: str | None = Field(default=None, description="참여 여부 ")
    memo: str | None = Field(default=None, description="메모")
    peer_name: str | None = Field(
        default=None, description="금액을 주거나 받은 상대방의 이름"
    )
    date: datetime | None = Field(default=None, description="금액을 주거나 받은 날짜")
    calendar_date: datetime | None = Field(default=None, description="경조사 일정")
    excel_id: int | None = Field(None, description="Excel ID")
    event_type_id: int | None = Field(default=None, description="경조사 ID")
    relation_id: int | None = Field(default=None, description="관계 ID")


class EditRecordDTOModel(EditRecordModel):
    id: int = Field(..., description="기록 ID")
