from fastapi import APIRouter, Depends, UploadFile

from app.core.dependencies import TenantAdminContext, require_tenant_admin
from app.core.storage import save_upload_file
from app.modules.menus.dependencies import get_menu_service
from app.modules.menus.schemas import (
    MenuItemCreateSchema,
    MenuItemReadSchema,
    MenuItemUpdateSchema,
    MenuReadSchema,
    MenuSectionCreateSchema,
    MenuSectionReadSchema,
    MenuSectionUpdateSchema,
)
from app.modules.menus.service import MenuService
from app.modules.tenants.public import TenantService, get_tenant_service

router = APIRouter(tags=["menus"])


@router.get("/tenants/{tenant_slug}/menu", response_model=MenuReadSchema)
async def get_menu(
    tenant_slug: str,
    service: MenuService = Depends(get_menu_service),
    tenant_service: TenantService = Depends(get_tenant_service),
) -> MenuReadSchema:
    tenant_id = await tenant_service.resolve_tenant_id(tenant_slug)
    return await service.get_menu_by_tenant_id(tenant_id)


@router.get("/backoffice/menu", response_model=MenuReadSchema)
async def get_backoffice_menu(
    current_admin: TenantAdminContext = Depends(require_tenant_admin),
    service: MenuService = Depends(get_menu_service),
) -> MenuReadSchema:
    return await service.get_menu_for_backoffice(current_admin.tenant_id)


@router.post("/backoffice/menu/sections", response_model=MenuSectionReadSchema, status_code=201)
async def create_section(
    payload: MenuSectionCreateSchema,
    current_admin: TenantAdminContext = Depends(require_tenant_admin),
    service: MenuService = Depends(get_menu_service),
) -> MenuSectionReadSchema:
    return await service.create_section(current_admin.tenant_id, payload)


@router.put("/backoffice/menu/sections/{section_id}", response_model=MenuSectionReadSchema)
async def update_section(
    section_id: str,
    payload: MenuSectionUpdateSchema,
    current_admin: TenantAdminContext = Depends(require_tenant_admin),
    service: MenuService = Depends(get_menu_service),
) -> MenuSectionReadSchema:
    return await service.update_section(section_id, payload)


@router.delete("/backoffice/menu/sections/{section_id}", status_code=204)
async def delete_section(
    section_id: str,
    current_admin: TenantAdminContext = Depends(require_tenant_admin),
    service: MenuService = Depends(get_menu_service),
) -> None:
    await service.delete_section(section_id)


@router.post(
    "/backoffice/menu/sections/{section_id}/items",
    response_model=MenuItemReadSchema,
    status_code=201,
)
async def create_item(
    section_id: str,
    payload: MenuItemCreateSchema,
    current_admin: TenantAdminContext = Depends(require_tenant_admin),
    service: MenuService = Depends(get_menu_service),
) -> MenuItemReadSchema:
    return await service.create_item(section_id, payload)


@router.put("/backoffice/menu/items/{item_id}", response_model=MenuItemReadSchema)
async def update_item(
    item_id: str,
    payload: MenuItemUpdateSchema,
    current_admin: TenantAdminContext = Depends(require_tenant_admin),
    service: MenuService = Depends(get_menu_service),
) -> MenuItemReadSchema:
    return await service.update_item(item_id, payload)


@router.delete("/backoffice/menu/items/{item_id}", status_code=204)
async def delete_item(
    item_id: str,
    current_admin: TenantAdminContext = Depends(require_tenant_admin),
    service: MenuService = Depends(get_menu_service),
) -> None:
    await service.delete_item(item_id)


@router.put("/backoffice/menu/items/{item_id}/photo", response_model=MenuItemReadSchema)
async def upload_item_photo(
    item_id: str,
    photo: UploadFile,
    current_admin: TenantAdminContext = Depends(require_tenant_admin),
    service: MenuService = Depends(get_menu_service),
) -> MenuItemReadSchema:
    photo_url = await save_upload_file(photo, subdirectory="menu-items")
    return await service.update_item_photo(item_id, photo_url)
