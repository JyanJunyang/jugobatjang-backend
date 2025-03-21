from functools import wraps
from typing import Any, Callable

from fastapi import Header
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """기본 response 구조"""

    status_code: int = 200
    data: Any | None = None
    message: str = "success"


class BaseHeader(BaseModel):
    """기본 헤더 구조"""

    version: str = Field(..., description="API 버전")
    access_token: str = Field(..., description="accessToken")
    refresh_token: str = Field(..., description="refreshToken")


def get_headers(
    version: str = Header(...),
    access_token: str = Header(...),
    refresh_token: str = Header(...),
) -> BaseHeader:
    return BaseHeader(
        version=version, access_token=access_token, refresh_token=refresh_token
    )


def add_token_to_response(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        """BaseResponse에서 token값이 있을 경우에만 반환하도록 데코레이터"""
        response = await func(*args, **kwargs)

        user_info = kwargs.get("user_info")
        token = user_info.get("token") if user_info else None

        if token:
            response_data = {"data": response.data, "token": token}
            return BaseResponse(data=response_data, status_code=200, message="success")

        return response

    return wrapper
