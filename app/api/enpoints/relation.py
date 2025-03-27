from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.core.database import get_db
from app.core.exceptions import (
    InvalidRequestErrorException,
    RequestDataMissingException,
)
from app.core.security import verify_token
from app.schema.base import BaseResponse, add_token_to_response
from app.schema.relation import (
    CreateRelationDTOModel,
    DelteRelationDTOModel,
    EditRelationDTOModel,
)
from app.services.relation_service import RelationService

router = APIRouter(prefix="/relation", tags=["relation"])


@router.post("")
@add_token_to_response
async def create_new_relation(
    req: CreateRelationDTOModel,
    user_info=Depends(verify_token),
    db: Session = Depends(get_db),
):
    """유저의 관계추가 API"""

    user_id = user_info.get("user_id")
    name, color_code = req.model_dump().values()

    rel = RelationService(db=db)

    rel.is_relation_exists(user_id=user_id, name=name)
    rel.allow_add_more(user_id=user_id)
    res = rel.insert_new_relation(user_id=user_id, name=name, color_code=color_code)

    return BaseResponse(data=res)


@router.get("")
@add_token_to_response
async def get_user_relations(
    user_info=Depends(verify_token), db: Session = Depends(get_db)
):
    """유저의 관계 조회하는 API."""
    user_id = user_info.get("user_id")
    token = user_info.get("token")
    rel = RelationService(db=db)
    data = rel.get_user_relations(user_id=user_id)
    return BaseResponse(data=data)


@router.patch("")
@add_token_to_response
async def edit_user_relation(
    req: EditRelationDTOModel,
    user_info=Depends(verify_token),
    db: Session = Depends(get_db),
):
    """관계 수정 로직"""

    relation_id, name, color_code = req.model_dump().values()

    if name is None and color_code is None:
        raise RequestDataMissingException(
            "name 또는 color_code 필드 중 하나는 반드시 포함되어야 합니다."
        )

    # 기본 관계 데이터 요청 시 InvalidRequestError
    if relation_id <= 101:
        raise InvalidRequestErrorException()

    rel = RelationService(db=db)
    data = rel.edit_user_relations(
        relation_id=relation_id, name=name, color_code=color_code
    )

    return BaseResponse(data=data)


@router.delete("")
@add_token_to_response
async def edit_user_relation(
    req: DelteRelationDTOModel,
    user_info=Depends(verify_token),
    db: Session = Depends(get_db),
):
    """관계 삭제 API"""
    relation_id = req.relation_id

    if relation_id <= 101:
        raise InvalidRequestErrorException()
    RelationService(db=db).delete_user_relation(relation_id=relation_id)
    return BaseResponse()
