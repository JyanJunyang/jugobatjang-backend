# 가입, 로그인

from typing import Annotated

from fastapi import APIRouter, Depends, Header, Request

from app.core.database import get_db
from app.schema.auth_schema import CommonHeader, SignUpDtoModel
from app.schema.base_response import BaseResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/kakao/callback")
async def kakao_callback(req: Request):
    """카카오 서버 테스트용 redirect 경로"""
    code = req.query_params.get("code")
    auth = AuthService()
    await auth.kakao_auth_callback(code=code)
    return {"code": code}


@router.post("/signup", response_model=BaseResponse)
async def sign_up(
    req: SignUpDtoModel,
    headers: Annotated[CommonHeader, Depends()],
    db=Depends(get_db),
) -> BaseResponse:
    """회원 가입 API"""
    auth = AuthService(db=db)

    # 로그인 타입에 따른 user_dat 분기처리
    if req.login_type == "KAKAO":
        social_user = await auth.get_kakao_user_info(access_token=headers.access_token)
        user_data = {**req.model_dump(), **social_user.model_dump()}

    # 신규유저 데이터 생성 후 user id값 반환
    user_id = await auth.signup_new_user(user_data=user_data)

    # user id값으로 jwt token 생성
    token = await auth.create_auth_token(
        data={
            "sub": user_id,
            "exp": headers.expires_in,
            "ref_exp": headers.refresh_expires_in,
        }
    )

    return BaseResponse(status_code=200, data=token, message="회원가입 완료.")
