from sqlalchemy import and_, or_
from sqlalchemy.orm.session import Session

from app.core.config import configs
from app.core.exceptions import (
    DataCreationNotAllowedException,
    DuplicatedErrorException,
)
from app.model.records import Relations
from app.schema.relation import UserRelationDTOModel
from app.util.limit_checker import can_add_more

MAX_RELATION_COUNT = configs.MAX_RELATION_COUNT


class RelationService:
    def __init__(self, db: Session):
        self.db = db

    def is_relation_exists(self, user_id: int, name: str):
        """이미 추가하려는 관계가 있는지 체크하는 메소드."""
        try:
            res = (
                self.db.query(Relations.id)
                .filter(
                    or_(
                        and_(Relations.name == name, Relations.user_id == user_id),
                        and_(Relations.name == name, Relations.user_id == None),
                    )
                )
                .first()
            )

            if res is not None:
                raise DuplicatedErrorException()

        except DuplicatedErrorException:
            raise
        except Exception as e:
            print(str(e))

    def allow_add_more(self, user_id: int):
        """관계데이터를 더 추가해도 되는지 체크하는 메소드."""
        try:
            count = (
                self.db.query(Relations.id)
                .filter(or_(Relations.user_id == user_id, Relations.user_id == None))
                .count()
            )

            if not can_add_more(count, int(MAX_RELATION_COUNT)):
                raise DataCreationNotAllowedException()

        except DataCreationNotAllowedException:
            raise

        except Exception as e:
            print(f"{str(e)}")

    def insert_new_relation(self, user_id: int, name: str, color_code: str):
        """새로운 관계 추가"""
        try:
            relations = Relations(user_id=user_id, name=name, color_code=color_code)
            self.db.add(relations)
            self.db.flush()
            self.db.refresh(relations)
            self.db.commit()
            return relations.id
        except Exception as e:
            self.db.rollback()
            print(str(e))
