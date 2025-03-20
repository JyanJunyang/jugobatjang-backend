from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.core.database import get_db
from app.core.security import verify_token
from app.schema.base import BaseResponse
from app.schema.relation import CreateRelationDTOModel
from app.services.relation_service import RelationService

router = APIRouter(prefix="/relation", tags=["relation"])


@router.post("")
async def create_new_relation(
    req: CreateRelationDTOModel,
    user_info=Depends(verify_token),
    db: Session = Depends(get_db),
):
    """유저의 관계추가 API"""

    user_id = user_info.get("user_id")
    name, color_code = req.name, req.color_code

    rel = RelationService(db=db)

    rel.is_relation_exists(user_id=user_id, name=name)
    rel.allow_add_more(user_id=user_id)
    res = rel.insert_new_relation(user_id=user_id, name=name, color_code=color_code)

    return BaseResponse(data=res)


@router.get("")
async def get_user_relations(
    user_info=Depends(verify_token), db: Session = Depends(get_db)
):
    """유저의 관계 조회하는 API."""
    user_id = user_info.get("user_id")
    rel = RelationService(db=db)
    res = rel.get_user_relations(user_id=user_id)

    return BaseResponse(data=res)
