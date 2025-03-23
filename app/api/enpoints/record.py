from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.core.database import get_db
from app.core.security import verify_token
from app.schema.base import BaseResponse, add_token_to_response
from app.schema.records import CreateRecordDTOModel
from app.services.record_service import RecordService

router = APIRouter(prefix="/record", tags=["record"])


@router.post("")
@add_token_to_response
async def create_new_record(
    req: CreateRecordDTOModel,
    user_info=Depends(verify_token),
    db: Session = Depends(get_db),
):
    """장부 기록하는 API"""
    user_id = user_info.get("user_id")
    record = RecordService(db=db).insert_new_record(req=req, user_id=user_id)
    return BaseResponse(data=record)
