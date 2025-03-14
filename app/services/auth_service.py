from datetime import datetime

import httpx
from jose import jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session

from app.core.config import configs
from app.core.exceptions import DuplicatedErrorException, UnknownErrorException
from app.model.users import Users
from app.schema.auth_schema import SocialUserDTOModel

KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"


class AuthService:
    def __init__(self, db: Session | None = None):
        self.db = db

    async def kakao_auth_callback(self, code):
        """카카오 소셜로그인 callback 메소드."""
        async with httpx.AsyncClient() as client:
            res = (
                await client.post(
                    url=KAKAO_AUTH_URL,
                    data={
                        "grant_type": "authorization_code",
                        "client_id": configs.KAKAO_API_KEY,
                        "redirect_uri": configs.KAKAO_REDIRECT_URI,
                        "code": code,
                    },
                )
            ).json()

        return res

    async def get_kakao_user_info(self, access_token: str) -> SocialUserDTOModel:
        """카카오 회원정보 가져오는 메소드."""

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url=KAKAO_USER_ME_URL,
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                        "Authorization": f"Bearer {access_token}",
                    },
                    params={"property_keys[]": "kakao_account.email"},
                )
                response.raise_for_status()  # HTTP 오류 응답 확인
                user = response.json()
            except httpx.HTTPStatusError as e:
                raise UnknownErrorException(
                    detail=f"카카오 API 호출 중 오류 발생: {str(e)}"
                )
            except httpx.RequestError as e:
                raise UnknownErrorException(
                    detail=f"카카오 API 요청 중 오류 발생: {str(e)}"
                )

            try:
                social_id = user.get("id")
                if not social_id:
                    raise ValueError("카카오 소셜 ID를 찾을 수 없습니다")

                account = user.get("kakao_account", {})
                email = account.get("email")
                profile = account.get("profile", {})
                name = profile.get("nickname")
                b_year = account.get("birthyear")
                b_day = account.get("birthday")
                birthday = None
                if b_year and b_day:
                    birthday = datetime.strptime(f"{b_year}{b_day}", "%Y-%m-%d")

            except (KeyError, TypeError) as e:
                raise UnknownErrorException(
                    detail=f"카카오 사용자 정보 파싱 중 오류 발생: {str(e)}"
                )

            return SocialUserDTOModel(
                social_id=f"{social_id}",
                email=email,
                name=name,
                birthday=birthday,
            )

    async def signup_new_user(self, user_data):
        """신규유저 생성 메소드."""
        try:
            user = Users(**user_data)
            self.db.add(user)
            self.db.flush()
            self.db.refresh(user)
            self.db.commit()

            return user.id
        except IntegrityError as e:
            if "for key 'users.email'" in str(e):
                raise DuplicatedErrorException(
                    detail="이미 사용 중인 이메일 주소입니다."
                )
            else:
                raise DuplicatedErrorException(str(e))
        except Exception as e:
            raise UnknownErrorException(detail=str(e))

    async def create_auth_token(self, data):
        """jwt token 생성 메소드."""
        to_encode = data.copy()
        exp = data.get("exp")
        ref_exp = data.get("ref_exp")
        to_encode.update({"exp": exp, "ref_exp": ref_exp})

        access_token = jwt.encode(
            to_encode, configs.SECRET_KEY, algorithm=configs.ALGORITHM
        )
        refresh_token = jwt.encode(
            to_encode, configs.REFRESH_SECRET_KEY, algorithm=configs.ALGORITHM
        )

        return dict(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=exp,
            refresh_expires_in=ref_exp,
        )
