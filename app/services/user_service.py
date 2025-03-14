from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session

from app.core.exceptions import (
    DuplicatedErrorException,
    NotFoundError,
    UnknownErrorException,
)
from app.model.users import Users


class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def is_registered_user(self, social_id: str) -> bool:
        """회원가입된 유저여부를 반환하는 메소드."""
        user = self.db.query(Users.id).filter(Users.social_id == social_id).first()
        if user is None:
            return False
        return True
