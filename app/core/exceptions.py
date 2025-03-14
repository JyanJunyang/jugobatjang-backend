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
