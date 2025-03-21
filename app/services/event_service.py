from sqlalchemy import and_, or_
from sqlalchemy.orm.session import Session

from app.core.config import configs
from app.core.exceptions import (
    DataCreationNotAllowedException,
    DuplicatedErrorException,
)
from app.model.records import EventTypes
from app.util.limit_checker import can_add_more

MAX_EVENTTYPE_COUNT = configs.MAX_EVENTTYPE_COUNT


class EventService:
    def __init__(self, db: Session):
        self.db = db

    # TODO Relation알 똑같은 로직 어떻게 통합시킬 지 고민 및 리팩토링 필요함.
    def is_event_exists(self, user_id: int, name: str):
        """이미 추가하려는 경조사가 있는지 체크하는 메소드."""
        try:
            res = (
                self.db.query(EventTypes.id)
                .filter(
                    or_(
                        and_(EventTypes.name == name, EventTypes.user_id == user_id),
                        and_(EventTypes.name == name, EventTypes.user_id == None),
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
        """경조사 데이터를 더 추가해도 되는지 체크하는 메소드."""
        try:
            count = (
                self.db.query(EventTypes.id)
                .filter(or_(EventTypes.user_id == user_id, EventTypes.user_id == None))
                .count()
            )

            if not can_add_more(count, int(MAX_EVENTTYPE_COUNT)):
                raise DataCreationNotAllowedException()

        except DataCreationNotAllowedException:
            raise

        except Exception as e:
            print(f"{str(e)}")

    def insert_new_event(self, user_id: int, name: str, color_code: str):
        """새로운 이벤트 추가"""
        try:
            event = EventTypes(user_id=user_id, name=name, color_code=color_code)
            self.db.add(event)
            self.db.flush()
            event.type_no = event.id
            self.db.commit()
            return event.id
        except Exception as e:
            self.db.rollback()
            print(str(e))
