from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.tenant_admins.schemas import TenantAdminLoginSchema, TenantAdminTokenSchema
from app.modules.tenant_admins import service

router = APIRouter(prefix="/backoffice/auth", tags=["backoffice-auth"])


@router.post("/login", response_model=TenantAdminTokenSchema)
async def login(
    payload: TenantAdminLoginSchema,
    session: AsyncSession = Depends(get_db_session),
) -> TenantAdminTokenSchema:
    return await service.login(session, payload)
