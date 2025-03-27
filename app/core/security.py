from datetime import datetime

from fastapi import Depends
from jose import ExpiredSignatureError, jwt

from app.core.config import configs
from app.core.exceptions import RequestDataMissingException, TokenExpiredException
from app.schema.base import BaseHeader

SECRET_KEY = configs.SECRET_KEY
ALGORITHM = configs.ALGORITHM
REFRESH_SECRET_KEY = configs.REFRESH_SECRET_KEY
ALGORITHM = configs.ALGORITHM

EXPIRE_IN = {
    "AOS": {"access": 259200, "refresh": 15768000},  # 3일, 6개월
    "WEB": {"access": 21600, "refresh": 86400},  # 6시간, 24시간
}

DEFAULT_EXPIRE = {"access": 21600, "refresh": 86400}


def get_expiration_time(is_access: bool, platform: str) -> int:
    """유효기간 반환하는 메소드."""

    current_time = int(datetime.now().timestamp())
    expire_times = EXPIRE_IN.get(platform, DEFAULT_EXPIRE)
    return current_time + expire_times["access" if is_access else "refresh"]


def create_jwt_token(data: dict, platform: str):
    """jwt token 반환하는 메소드."""
    to_encode = data.copy()

    access_exp = get_expiration_time(is_access=True, platform=platform)
    refresh_exp = get_expiration_time(is_access=False, platform=platform)

    access_token = jwt.encode(
        {**to_encode, "exp": access_exp}, SECRET_KEY, algorithm=ALGORITHM
    )
    refresh_token = jwt.encode(
        {**to_encode, "exp": refresh_exp}, REFRESH_SECRET_KEY, algorithm=ALGORITHM
    )

    return access_token, refresh_token


def verify_token(headers: BaseHeader = Depends()):
    """API 회원 인증 검증 메소드. (주입해서 처리할 예정)"""
    access_token = headers.access_token
    refresh_token = headers.refresh_token

    if access_token is None or refresh_token is None:
        raise RequestDataMissingException()

    platform = headers.platform
    res = decode_jwt_payload(
        access_token=access_token, refresh_token=refresh_token, platform=platform
    )
    return res


def decode_jwt_payload(access_token: str, refresh_token: str, platform: str):
    """token decoding 후 user_id값 반환"""
    try:
        if not access_token or not refresh_token:
            raise RequestDataMissingException(detail="토큰이 필요합니다.")
        # access_token 디코딩
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = int(payload.get("sub"))
        return dict(user_id=user_id)
    except ExpiredSignatureError:
        try:
            # access_token 만료 시 refresh_token으로 token 갱신 및 user_id값 반환
            payload = jwt.decode(
                refresh_token, REFRESH_SECRET_KEY, algorithms=ALGORITHM
            )
            user_id = payload.get("sub")
            data = {
                "sub": user_id,
            }

            access_token, refresh_token = create_jwt_token(data=data, platform=platform)

            return dict(user_id=user_id, token={**access_token, **refresh_token})
        except ExpiredSignatureError:
            # refresh_token도 만료됐을 경우 raise exception
            raise TokenExpiredException() from None
