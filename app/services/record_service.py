from typing import List

from sqlalchemy.orm.session import Session

from app.core.database import convert_page_to_offset, convert_rows_to_dict_list
from app.model.records import EventTypes, Records, Relations
from app.schema.records import CreateRecordDTOModel, RecordSearchResponseDTOModel


class RecordService:
    def __init__(self, db: Session):
        self.db = db

    def insert_new_record(self, req: CreateRecordDTOModel, user_id: int):
        """경조사 기록 생성 메소드."""
        try:
            record = Records(**req.model_dump(), user_id=user_id)
            self.db.add(record)
            self.db.flush()
            record_id = record.id
            self.db.commit()
            return record_id
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
