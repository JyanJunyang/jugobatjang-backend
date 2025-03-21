from pydantic import BaseModel
from sqlmodel import Field


class CreateEventDTOModel(BaseModel):
    """경조사 생성 DTO"""

    name: str = Field(..., description="경조사 이름")
    color_code: str = Field(..., description="경조사 커스텀 색상")


class UserEventDTOModel(BaseModel):
    """유저의 경조사 DTO"""

    event_id: int = Field(..., description="경조사 id")
    name: str = Field(..., description="경조사 이름")
    color_code: str = Field(..., description="경조사 커스텀 색상")


class EditEventDTOModel(BaseModel):
    """경조사 수정 DTO"""

    event_id: int = Field(..., description="경조사 id")
    name: str | None = Field(default=None, description="경조사 이름")
    color_code: str | None = Field(default=None, description="경조사 커스텀 색상")


class DelteEventDTOModel(BaseModel):
    """경조사 삭제 DTO"""

    event_id: int = Field(..., description="경조사 id")
