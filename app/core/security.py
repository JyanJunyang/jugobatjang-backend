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


def verify_token(headers: BaseHeader = Depends()):
    """API 회원 인증 검증 메소드. (주입해서 처리할 예정)"""
    access_token = headers.access_token
    refresh_token = headers.refresh_token

    if access_token is None or refresh_token is None:
        raise RequestDataMissingException()

    res = decode_jwt_payload(access_token=access_token, refresh_token=refresh_token)
    return res


def create_jwt_access_token(data):
    """access_token 생성 메소드."""

    to_encode = data.copy()
    exp = int(datetime.now().timestamp()) + 86400  # 1일
    to_encode.update({"exp": exp})

    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return dict(access_token=access_token)


def create_jwt_refresh_token(data):
    """refresh_token 생성 메소드."""
    to_encode = data.copy()
    exp = int(datetime.now().timestamp()) + 259200  # 3일
    to_encode.update({"exp": exp})

    refresh_token = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

    return dict(refresh_token=refresh_token)


def decode_jwt_payload(access_token: str, refresh_token: str):
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
            access_token = create_jwt_access_token(data=data)
            refresh_token = create_jwt_refresh_token(data=data)
            return dict(user_id=user_id, token={**access_token, **refresh_token})
        except ExpiredSignatureError:
            # refresh_token도 만료됐을 경우 raise exception
            raise TokenExpiredException() from None
