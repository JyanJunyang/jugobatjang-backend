from pydantic import BaseModel
from sqlmodel import Field


class CreateRelationDTOModel(BaseModel):
    name: str = Field(..., description="관계 이름")
    color_code: str = Field(..., description="관계 커스텀 색상")
