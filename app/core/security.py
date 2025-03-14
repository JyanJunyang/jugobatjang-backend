from datetime import datetime

from jose import ExpiredSignatureError, jwt

from app.core.config import configs
from app.core.exceptions import RequestDataMissingException, TokenExpiredException

SECRET_KEY = configs.SECRET_KEY
ALGORITHM = configs.ALGORITHM
REFRESH_SECRET_KEY = configs.REFRESH_SECRET_KEY
ALGORITHM = configs.ALGORITHM


def create_jwt_access_token(data):
    """access_token 생성 메소드."""

    to_encode = data.copy()
    exp = int(datetime.now().timestamp()) + 86400  # 1일
    to_encode.update({"exp": exp})

    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return dict(access_token=access_token, expires_in=exp)
