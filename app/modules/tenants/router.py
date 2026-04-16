from fastapi import APIRouter, Depends

from app.core.dependencies import TenantAdminContext, require_tenant_admin
from app.modules.tenants.dependencies import get_tenant_service
from app.modules.tenants.schemas import (
    TenantSettingsReadSchema,
    TenantSettingsUpdateSchema,
    TenantThemeReadSchema,
    TenantThemeUpdateSchema,
)
from app.modules.tenants.service import TenantService

router = APIRouter(tags=["tenants"])


@router.get("/tenants/{tenant_slug}/theme", response_model=TenantThemeReadSchema)
async def get_tenant_theme(
    tenant_slug: str,
    service: TenantService = Depends(get_tenant_service),
) -> TenantThemeReadSchema:
    return await service.get_theme_by_tenant_slug(tenant_slug)


@router.get("/tenants/{tenant_slug}/settings", response_model=TenantSettingsReadSchema)
async def get_tenant_settings(
    tenant_slug: str,
    service: TenantService = Depends(get_tenant_service),
) -> TenantSettingsReadSchema:
    return await service.get_settings_by_tenant_slug(tenant_slug)


@router.put("/backoffice/theme", response_model=TenantThemeReadSchema)
async def update_theme(
    payload: TenantThemeUpdateSchema,
    current_admin: TenantAdminContext = Depends(require_tenant_admin),
    service: TenantService = Depends(get_tenant_service),
) -> TenantThemeReadSchema:
    return await service.update_theme(current_admin.tenant_id, payload)


@router.put("/backoffice/settings", response_model=TenantSettingsReadSchema)
async def update_settings(
    payload: TenantSettingsUpdateSchema,
    current_admin: TenantAdminContext = Depends(require_tenant_admin),
    service: TenantService = Depends(get_tenant_service),
) -> TenantSettingsReadSchema:
    return await service.update_settings(current_admin.tenant_id, payload)
