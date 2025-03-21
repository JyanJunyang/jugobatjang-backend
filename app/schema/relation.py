from pydantic import BaseModel
from sqlmodel import Field


class CreateRelationDTOModel(BaseModel):
    """관계 생성 DTO"""

    name: str = Field(..., description="관계 이름")
    color_code: str = Field(..., description="관계 커스텀 색상")


class UserRelationDTOModel(BaseModel):
    """유저의 관계 DTO"""

    relation_id: int = Field(..., description="관계 id")
    name: str = Field(..., description="관계 이름")
    color_code: str = Field(..., description="관계 커스텀 색상")


class EditRelationDTOModel(BaseModel):
    """관계 수정 DTO"""

    relation_id: int = Field(..., description="관계 id")
    name: str | None = Field(default=None, description="관계 이름")
    color_code: str | None = Field(default=None, description="관계 커스텀 색상")


class DelteRelationDTOModel(BaseModel):
    """관계 삭제 DTO"""

    relation_id: int = Field(..., description="관계 id")
