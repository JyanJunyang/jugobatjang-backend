from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.core.database import get_db
from app.core.security import verify_token
from app.schema.base import BaseResponse, add_token_to_response
from app.schema.event import CreateEventDTOModel
from app.services.event_service import EventService

router = APIRouter(prefix="/event", tags=["event"])


@router.post("")
@add_token_to_response
async def create_new_relation(
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
