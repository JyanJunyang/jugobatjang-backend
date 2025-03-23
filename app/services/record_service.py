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
