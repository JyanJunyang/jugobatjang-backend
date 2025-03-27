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

    async def get_user_id(self, social_id: str):
        """social_id값으로 user_id값 반환하는 메소드."""
        user = self.db.query(Users.id).filter(Users.social_id == social_id).first()
        if user is None:
            raise NotFoundError(detail="해당 사용자를 찾을 수 없습니다.")
        return user.id

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
            self.db.rollback()
            error_msg = str(e).lower()
            if "duplicate entry" in error_msg and "email" in error_msg:
                raise DuplicatedErrorException(
                    detail="이미 사용 중인 이메일 주소입니다."
                ) from e
        except Exception as e:
            self.db.rollback()
            raise UnknownErrorException(detail=str(e)) from e
