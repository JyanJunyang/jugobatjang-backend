from typing import Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    """기본 response 구조"""

    status_code: int
    data: Any
    message: str
