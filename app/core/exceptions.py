from typing import Any, Dict, Optional

from fastapi import HTTPException, status
from pydantic import ValidationError


class DuplicatedErrorException(HTTPException):
    """중복된 데이터 오류"""

    def __init__(
        self, detail: Optional[str] = None, headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, headers)


class UnknownErrorException(HTTPException):
    """알 수 없는 서버오류"""

    def __init__(
        self, detail: Optional[str] = None, headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail, headers)


class NotFoundError(HTTPException):
    """찾을 수 없는 데이터 오류"""

    def __init__(
        self, detail: Optional[str] = None, headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status.HTTP_404_NOT_FOUND, detail, headers)


class TokenExpiredException(HTTPException):
    """토큰 만료 오류"""

    def __init__(self, detail="토큰이 만료되었습니다.", headers=None):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, headers)
