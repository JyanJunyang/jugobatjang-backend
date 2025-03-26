from datetime import datetime

from sqlalchemy.orm.session import Session

from app.core.database import (
    convert_page_to_offset,
    convert_row_to_dict,
    convert_rows_to_dict_list,
)
from app.core.exceptions import NotFoundError
from app.model.calendar import Calendar
from app.model.records import EventTypes, Records, Relations
from app.schema.calendar import CreateCalendarDTOModel
from app.schema.records import (
    CreateRecordDTOModel,
    RecordDetailDTOModel,
    RecordSearchResponseDTOModel,
)


class RecordService:
    def __init__(self, db: Session):
        self.db = db

    def insert_new_record(self, req: CreateRecordDTOModel, user_id: int):
        """경조사 기록 생성 및 캘린더 생성 메소드."""

        try:
            record = Records(**req.model_dump(), user_id=user_id)
            self.db.add(record)
            self.db.flush()
            record_id = record.id
            self.db.commit()

            # 캘린더 생성
            self.insert_new_calendar_by_record(req, record_id, user_id)

            return record_id

        except Exception as e:
            self.db.rollback()
            print(f"error : {str(e)}")

    def insert_new_calendar_by_record(
        self, req: CreateRecordDTOModel, record_id: int, user_id: int
    ):
        """캘린더 데이터 생성 메소드."""

        calendar_date = req.calendar_date
        if calendar_date:
            peer_name = req.peer_name
            event_type_id = req.event_type_id
            event_name = self.get_event_name_by_id(event_type_id)
            title = f"{peer_name} {event_name}"

            calendar = CreateCalendarDTOModel(
                title=title, date=calendar_date, user_id=user_id, record_id=record_id
            )
            calendar = Calendar(**calendar.model_dump())
            self.db.add(calendar)
            self.db.commit()

    def get_event_name_by_id(self, event_type_id: int):
        """id값으로 경조사 이름 조회하는 메소드."""
        try:
            return (
                self.db.query(EventTypes.name)
                .filter(EventTypes.id == event_type_id)
                .scalar()
            )
        except Exception as e:
            print(f"error : {str(e)}")

    # TODO 🚀 : 성능개선 반드시 필요
    # 멀티인덱스 처리 우선적으로
    # TODO 🚀 : 페이징 처리도 성능개선 반드시 필요!
    def get_user_records(
        self,
        user_id: int,
        is_received: int,
        page: int,
        size: int,
        event_types: str | None = None,
        relations: str | None = None,
    ):
        """유저의 경조사 기록 조회하는 메소드."""
        try:
            query = (
                self.db.query(
                    Records.id,
                    Records.name,
                    Records.amount,
                    Records.event_date,
                    Records.created_at,
                    EventTypes.name.label("event_type_name"),
                    Relations.name.label("relation_name"),
                )
                .join(EventTypes, Records.event_type_id == EventTypes.id, isouter=True)
                .join(Relations, Records.relation_id == Relations.id, isouter=True)
                .filter(
                    Records.user_id == user_id,
                    Records.is_received == is_received,
                )
            )

            if event_types:
                event_types = list(map(int, event_types.split(",")))
                query = query.filter(Records.event_type_id.in_(event_types))
            if relations:
                relations = list(map(int, relations.split(",")))
                query = query.filter(Records.relation_id.in_(relations))

            offset = convert_page_to_offset(size=size, page=page)
            query = query.limit(size).offset(offset)
            res = query.all()

            return convert_rows_to_dict_list(
                query_result=res, dto_class=RecordSearchResponseDTOModel
            )
        except Exception as e:
            print(str(e))

    def get_record_detail(self, user_id: int, record_id: int):
        """기록 상세조회하는 메소드."""
        try:
            res = (
                self.db.query(
                    Records.id,
                    Records.name,
                    Records.amount,
                    Records.is_received,
                    Records.phone,
                    Records.status,
                    Records.memo,
                    Records.event_date,
                    Records.created_at,
                    EventTypes.id.label("event_type_id"),
                    EventTypes.name.label("event_type_name"),
                    EventTypes.color_code.label("event_type_color_code"),
                    Relations.id.label("relation_id"),
                    Relations.name.label("relation_name"),
                    Relations.color_code.label("relation_color_code"),
                )
                .join(EventTypes, Records.event_type_id == EventTypes.id, isouter=True)
                .join(Relations, Records.relation_id == Relations.id, isouter=True)
                .filter(
                    Records.id == record_id,
                    Records.user_id == user_id,
                )
            ).first()

            return convert_row_to_dict(res, RecordDetailDTOModel)
        except Exception as e:
            print(str(e))

    def edit_user_record(
        self,
        user_id: int,
        id: int,
        name: str | None = None,
        amount: int | None = None,
        is_received: int | None = None,
        phone: str | None = None,
        status: str | None = None,
        memo: str | None = None,
        event_date: datetime | None = None,
        excel_id: int | None = None,
        event_type_id: int | None = None,
        relation_id: int | None = None,
    ):
        """기록 수정하는 메소드."""
        try:
            record = (
                self.db.query(Records)
                .filter(Records.id == id, Records.user_id == user_id)
                .first()
            )

            if record is None:
                raise NotFoundError()

            update_data = {
                "name": name,
                "amount": amount,
                "is_received": is_received,
                "phone": phone,
                "status": status,
                "memo": memo,
                "event_date": event_date,
                "excel_id": excel_id,
                "event_type_id": event_type_id,
                "relation_id": relation_id,
            }

            for key, value in update_data.items():
                if value is not None:
                    setattr(record, key, value)

            self.db.commit()

        except Exception as e:
            print(str(e))

    def delete_user_record(self, record_id: int):
        """기록 삭제 메소드."""
        try:
            self.db.query(Records).filter(Records.id == record_id).delete()
            self.db.commit()
        except Exception as e:
            print(f"error : {str(e)}")
