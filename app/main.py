from fastapi import FastAPI

from app.api.enpoints.auth import router as auth_router
from app.api.enpoints.record import router as record_router
from app.core.exceptions import (
    DuplicatedErrorException,
    NotFoundError,
    RequestDataMissingException,
    TokenExpiredException,
    UnknownErrorException,
    exception_handler,
)

app = FastAPI(
    title="주고받장 API",
    description="주고받장 API 문서입니다. version 관리는 path에 녹이도록 하겠습니다.",
)

app.include_router(auth_router)
app.include_router(record_router)

app.add_exception_handler(DuplicatedErrorException, exception_handler)
app.add_exception_handler(UnknownErrorException, exception_handler)
app.add_exception_handler(NotFoundError, exception_handler)
app.add_exception_handler(TokenExpiredException, exception_handler)
app.add_exception_handler(RequestDataMissingException, exception_handler)
