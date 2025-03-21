from typing import Any, Dict, Optional

from fastapi import status
from fastapi.responses import JSONResponse

from app.schema.base import BaseResponse


class CustomException(Exception):
    """커스텀 예외 기본 클래스"""

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DEFAULT_MESSAGE = "오류가 발생했습니다."

    def __init__(
        self, detail: Optional[str] = None, headers: Optional[Dict[str, Any]] = None
    ):
        self.response = BaseResponse(
            status_code=self.STATUS_CODE, message=detail or self.DEFAULT_MESSAGE
        )
        self.headers = headers


class DuplicatedErrorException(CustomException):
    """중복된 데이터 오류"""

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DEFAULT_MESSAGE = "이미 존재하는 데이터입니다."


class UnknownErrorException(CustomException):
    """알 수 없는 서버 오류"""

    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DEFAULT_MESSAGE = "서버 내부 오류가 발생했습니다."


class NotFoundError(CustomException):
    """찾을 수 없는 데이터 오류"""

    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DEFAULT_MESSAGE = "데이터를 찾을 수 없습니다."


class TokenExpiredException(CustomException):
    """토큰 만료 오류"""

    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DEFAULT_MESSAGE = "토큰이 만료되었습니다."


class RequestDataMissingException(CustomException):
    """필수 요청 파라미터 누락 오류"""

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DEFAULT_MESSAGE = "필수 요청 파라미터 누락"

    def __init__(self, detail: Optional[str] = None):
        super().__init__(
            detail=f"{self.DEFAULT_MESSAGE} : {detail}" or self.DEFAULT_MESSAGE
        )


class DataCreationNotAllowedException(CustomException):
    """데이터 생성 불가 오류"""

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DEFAULT_MESSAGE = "데이터를 더 이상 생성할 수 없습니다."


async def exception_handler(_, exc: Exception):
    """CustomException 예외 발생 시 처리"""
    return JSONResponse(
        status_code=exc.response.status_code,
        content=exc.response.model_dump(),
        headers=exc.headers,
    )
