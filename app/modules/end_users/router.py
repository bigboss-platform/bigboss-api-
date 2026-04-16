from fastapi import APIRouter, Depends

from app.core.dependencies import EndUserContext, require_end_user
from app.modules.end_users.dependencies import get_end_user_service
from app.modules.end_users.schemas import EndUserReadSchema, EndUserUpdateSchema
from app.modules.end_users.service import EndUserService

router = APIRouter(prefix="/end-users", tags=["end-users"])


@router.get("/me", response_model=EndUserReadSchema)
async def get_current_end_user(
    current_user: EndUserContext = Depends(require_end_user),
    service: EndUserService = Depends(get_end_user_service),
) -> EndUserReadSchema:
    return await service.get_by_id(current_user.end_user_id)


@router.put("/me", response_model=EndUserReadSchema)
async def update_current_end_user(
    payload: EndUserUpdateSchema,
    current_user: EndUserContext = Depends(require_end_user),
    service: EndUserService = Depends(get_end_user_service),
) -> EndUserReadSchema:
    return await service.update(current_user.end_user_id, payload)
