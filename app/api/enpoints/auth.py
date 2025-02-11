# 가입, 로그인

from fastapi import APIRouter

from app.schema.auth_schema import SignInResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign-in", response_model=SignInResponse)
def sign_in():
    """로그인 API"""
    return dict(message="이건 auth")
