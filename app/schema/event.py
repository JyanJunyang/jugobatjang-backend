from pydantic import BaseModel
from sqlmodel import Field


class CreateEventDTOModel(BaseModel):
    """경조사 생성 DTO"""

    name: str = Field(..., description="경조사 이름")
    color_code: str = Field(..., description="경조사 커스텀 색상")
