from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.tenants.models import Tenant, TenantSettings, TenantTheme


class TenantRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_slug(self, slug: str) -> Tenant | None:
        result = await self._session.execute(
            select(Tenant).where(Tenant.slug == slug, Tenant.is_deleted == False)  # noqa: E712
        )
        return result.scalar_one_or_none()

    async def find_theme_by_tenant_id(self, tenant_id: str) -> TenantTheme | None:
        result = await self._session.execute(
            select(TenantTheme).where(TenantTheme.tenant_id == tenant_id)
        )
        return result.scalar_one_or_none()

    async def find_settings_by_tenant_id(self, tenant_id: str) -> TenantSettings | None:
        result = await self._session.execute(
            select(TenantSettings).where(TenantSettings.tenant_id == tenant_id)
        )
        return result.scalar_one_or_none()

    async def save(self, entity: Tenant | TenantTheme | TenantSettings) -> None:
        self._session.add(entity)
        await self._session.flush()
