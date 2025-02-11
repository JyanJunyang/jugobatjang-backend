from fastapi import FastAPI

from app.api.enpoints.auth import router as auth_router

app = FastAPI(
    title="주고받장 API",
    description="주고받장 API 문서입니다. version 관리는 path에 녹이도록 하겠습니다.",
)


@app.get("/")
def test():
    return dict(message="API 테스트")


app.include_router(auth_router)
