import datetime
from pydantic import BaseModel

class SignInResponse(BaseModel):
    access_token : str
    expiration : str #FIXME : 이거 pydantic에 맞는? datet타입으로 변경필요
    # user_info : User