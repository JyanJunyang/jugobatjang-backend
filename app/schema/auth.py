from datetime import datetime

from pydantic import BaseModel, Field


class AuthDTOModel(BaseModel):
    """회원가입, 로그인 DTO"""

    login_type: str = Field(..., description="로그인 유형 (KAKAO, EMAIL)")
    social_id: str | None = Field(None, description="소셜로그인 시 id값")
    email: str | None = Field(
        None,
        description="이메일 주소 (이메일 로그인일 경우 필수)",
    )
    password: str | None = Field(
        None, description="비밀번호 (이메일 로그인일 경우 필수)"
    )


class CommonHeader(BaseModel):
    token_type: str | None = Field(None, description="토큰 타입")
    access_token: str | None = Field(None, description="액세스 토큰")
    refresh_token: str | None = Field(None, description="액세스 리프레쉬 토큰")
    expires_in: str | None = Field(None, description="토큰 만료시간(초)")
    refresh_expires_in: str | None = Field(
        None, description="리프레쉬 토큰 만료시간(초)"
    )


class SocialUserDTOModel(BaseModel):
    """소셜 로그인으로 가져오는 회원 정보"""

    social_id: str = Field(..., description="소셜 id")
    email: str = Field(..., description="이메일 주소")
    name: str | None = Field(description="유저 이름")
    birthday: datetime | None = Field(description="유저의 생일", examples="YYYY-MM-DD")
