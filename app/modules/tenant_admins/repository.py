from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.tenant_admins.models import TenantAdmin


async def find_by_email(session: AsyncSession, email: str) -> TenantAdmin | None:
    result = await session.execute(
        select(TenantAdmin).where(
            TenantAdmin.email == email,
            TenantAdmin.is_deleted == False,  # noqa: E712
        )
    )
    return result.scalar_one_or_none()


async def find_by_id(session: AsyncSession, admin_id: str) -> TenantAdmin | None:
    result = await session.execute(
        select(TenantAdmin).where(
            TenantAdmin.id == admin_id,
            TenantAdmin.is_deleted == False,  # noqa: E712
        )
    )
    return result.scalar_one_or_none()
