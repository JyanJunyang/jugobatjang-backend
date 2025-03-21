from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.core.database import get_db
from app.core.exceptions import InvalidRequestError, RequestDataMissingException
from app.core.security import verify_token
from app.schema.base import BaseResponse, add_token_to_response
from app.schema.event import CreateEventDTOModel, DelteEventDTOModel, EditEventDTOModel
from app.services.event_service import EventService

router = APIRouter(prefix="/event", tags=["event"])


@router.post("")
@add_token_to_response
async def create_new_event(
    req: CreateEventDTOModel,
    user_info=Depends(verify_token),
    db: Session = Depends(get_db),
):
    """유저의 관계추가 API"""

    user_id = user_info.get("user_id")
    name, color_code = req.model_dump().values()

    event = EventService(db=db)
    event.is_event_exists(user_id=user_id, name=name)
    event.allow_add_more(user_id=user_id)
    res = event.insert_new_event(user_id=user_id, name=name, color_code=color_code)

    return BaseResponse(data=res)


@router.get("")
@add_token_to_response
async def get_user_events(
    user_info=Depends(verify_token), db: Session = Depends(get_db)
):
    """유저의 관계 조회하는 API."""
    user_id = user_info.get("user_id")
    event = EventService(db=db)
    data = event.get_user_events(user_id=user_id)
    return BaseResponse(data=data)


@router.patch("")
@add_token_to_response
async def edit_user_event(
    req: EditEventDTOModel,
    user_info=Depends(verify_token),
    db: Session = Depends(get_db),
):
    """관계 수정 로직"""

    event_id, name, color_code = req.model_dump().values()

    if name is None and color_code is None:
        raise RequestDataMissingException(
            "name 또는 color_code 필드 중 하나는 반드시 포함되어야 합니다."
        )

    if event_id <= 101:
        raise InvalidRequestError()

    event = EventService(db=db)
    data = event.edit_user_event(event_id=event_id, name=name, color_code=color_code)

    return BaseResponse(data=data)


@router.delete("")
@add_token_to_response
async def edit_user_event(
    req: DelteEventDTOModel,
    user_info=Depends(verify_token),
    db: Session = Depends(get_db),
):
    """관계 삭제 API"""
    event_id = req.event_id

    if event_id <= 101:
        raise InvalidRequestError()
    EventService(db=db).delete_user_event(event_id=event_id)
    return BaseResponse()
