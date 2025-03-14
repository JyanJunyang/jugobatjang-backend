from typing import Any

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """기본 response 구조"""

    status_code: int
    data: Any | None = None
    message: str = "success"


class BaseHeader(BaseModel):
    """기본 헤더 구조"""

    version: str = Field(..., description="API 버전")
    access_token: str = Field(..., description="accessToken")
    refresh_token: str = Field(..., description="refreshToken")
