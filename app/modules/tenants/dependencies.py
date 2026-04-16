from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.tenants.repository import TenantRepository
from app.modules.tenants.service import TenantService


def get_tenant_repository(session: AsyncSession = Depends(get_db_session)) -> TenantRepository:
    return TenantRepository(session=session)


def get_tenant_service(
    repository: TenantRepository = Depends(get_tenant_repository),
) -> TenantService:
    return TenantService(repository=repository)
