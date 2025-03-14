from typing import Any

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """기본 response 구조"""

    status_code: int
    data: Any | None = None
    message: str = "success"
