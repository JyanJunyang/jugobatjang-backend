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


@router.get("")
@add_token_to_response
async def get_user_records(
    is_received: str,
    page: int = 1,
    size: int = 10,
    event_types: str | None = None,
    relations: str | None = None,
    user_info=Depends(verify_token),
    db: Session = Depends(get_db),
):
    """기록 조회하는 API."""
    user_id = user_info.get("user_id")

    records = RecordService(db=db).get_user_records(
        user_id=user_id,
        is_received=is_received,
        page=page,
        size=size,
        event_types=event_types,
        relations=relations,
    )
    return BaseResponse(data=records)


@router.get("{id}")
@add_token_to_response
async def get_record_detail(
    id: str,
    user_info=Depends(verify_token),
    db: Session = Depends(get_db),
):
    """기록 상세 조회"""
    user_id = user_info.get("user_id")
    record = RecordService(db=db).get_record_detail(user_id=user_id, record_id=id)
    return BaseResponse(data=record)
