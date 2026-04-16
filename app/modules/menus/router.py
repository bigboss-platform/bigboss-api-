from fastapi import APIRouter, Depends

from app.modules.menus.dependencies import get_menu_service
from app.modules.menus.schemas import MenuReadSchema
from app.modules.menus.service import MenuService

router = APIRouter(tags=["menus"])


@router.get("/tenants/{tenant_slug}/menu", response_model=MenuReadSchema)
async def get_menu(
    tenant_slug: str,
    service: MenuService = Depends(get_menu_service),
) -> MenuReadSchema:
    return await service.get_menu_by_tenant_id(tenant_slug)
