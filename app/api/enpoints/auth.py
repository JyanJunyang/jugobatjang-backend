from fastapi import APIRouter, Depends, Header, Request

from app.core.database import get_db
from app.core.security import create_jwt_access_token, create_jwt_refresh_token
from app.schema.auth import AuthDTOModel
from app.schema.base import BaseHeader, BaseResponse, get_headers
from app.services.auth_service import AuthService
from app.services.user_service import UserService

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


@router.post("/signin", response_model=BaseResponse)
async def sign_in(
    req: AuthDTOModel,
    headers: BaseHeader = Depends(get_headers),
    db=Depends(get_db),
):
    """소셜ID값으로 회원여부를 확인하고, 없으면 가입 후 자체 JWT 발급하는 API."""
    user = UserService(db=db)
    is_registered = await user.is_registered_user(social_id=req.social_id)

    auth = AuthService()
    access_token = headers.access_token
    refresh_token = headers.refresh_token

    if is_registered:
        social_user = await auth.get_kakao_user_info(access_token=access_token)
        social_id = social_user.social_id
        user_id = await user.get_user_id(social_id=social_id)
    else:
        social_user = await auth.get_kakao_user_info(access_token=access_token)
        user_data = {**req.model_dump(), **social_user.model_dump()}
        user_id = await user.signup_new_user(user_data=user_data)

    data = {
        "sub": f"{user_id}",
    }
    access_token = create_jwt_access_token(data=data)
    refresh_token = create_jwt_refresh_token(data=data)

    token = {**access_token, **refresh_token}

    return BaseResponse(status_code=200, data=token)
