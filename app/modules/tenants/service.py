from app.modules.tenants.exceptions import TenantNotFoundException, TenantThemeNotFoundException
from app.modules.tenants.repository import TenantRepository
from app.modules.tenants.schemas import (
    TenantSettingsReadSchema,
    TenantSettingsUpdateSchema,
    TenantThemeReadSchema,
    TenantThemeUpdateSchema,
)


class TenantService:
    def __init__(self, repository: TenantRepository) -> None:
        self._repository = repository

    async def get_theme_by_tenant_slug(self, tenant_slug: str) -> TenantThemeReadSchema:
        tenant = await self._repository.find_by_slug(tenant_slug)
        if tenant is None:
            raise TenantNotFoundException(tenant_slug)
        theme = await self._repository.find_theme_by_tenant_id(tenant.id)
        if theme is None:
            raise TenantThemeNotFoundException(tenant.id)
        return TenantThemeReadSchema.model_validate(theme)

    async def get_settings_by_tenant_slug(self, tenant_slug: str) -> TenantSettingsReadSchema:
        tenant = await self._repository.find_by_slug(tenant_slug)
        if tenant is None:
            raise TenantNotFoundException(tenant_slug)
        settings_record = await self._repository.find_settings_by_tenant_id(tenant.id)
        if settings_record is None:
            raise TenantNotFoundException(tenant_slug)
        return TenantSettingsReadSchema.model_validate(settings_record)

    async def update_theme(
        self, tenant_id: str, payload: TenantThemeUpdateSchema
    ) -> TenantThemeReadSchema:
        theme = await self._repository.find_theme_by_tenant_id(tenant_id)
        if theme is None:
            raise TenantThemeNotFoundException(tenant_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(theme, field, value)
        await self._repository.save(theme)
        return TenantThemeReadSchema.model_validate(theme)

    async def get_settings_by_tenant_id(self, tenant_id: str) -> TenantSettingsReadSchema:
        settings_record = await self._repository.find_settings_by_tenant_id(tenant_id)
        if settings_record is None:
            raise TenantNotFoundException(tenant_id)
        return TenantSettingsReadSchema.model_validate(settings_record)

    async def resolve_tenant_id(self, slug: str) -> str:
        tenant = await self._repository.find_by_slug(slug)
        if tenant is None:
            raise TenantNotFoundException(slug)
        return tenant.id

    async def update_settings(
        self, tenant_id: str, payload: TenantSettingsUpdateSchema
    ) -> TenantSettingsReadSchema:
        settings_record = await self._repository.find_settings_by_tenant_id(tenant_id)
        if settings_record is None:
            raise TenantNotFoundException(tenant_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(settings_record, field, value)
        await self._repository.save(settings_record)
        return TenantSettingsReadSchema.model_validate(settings_record)
