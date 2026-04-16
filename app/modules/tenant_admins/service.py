from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.modules.tenant_admins import repository
from app.modules.tenant_admins.schemas import TenantAdminLoginSchema, TenantAdminTokenSchema, TenantAdminReadSchema
from app.modules.tenant_admins.exceptions import InvalidCredentialsException, TenantAdminInactiveException
from app.core.security import create_access_token, create_refresh_token

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def login(session: AsyncSession, payload: TenantAdminLoginSchema) -> TenantAdminTokenSchema:
    admin = await repository.find_by_email(session, payload.email)
    if admin is None:
        raise InvalidCredentialsException()

    if not _pwd_context.verify(payload.password, admin.password_hash):
        raise InvalidCredentialsException()

    if not admin.is_active:
        raise TenantAdminInactiveException()

    return TenantAdminTokenSchema(
        access_token=create_access_token(
            subject=str(admin.id),
            role="tenant_admin",
            tenant_id=str(admin.tenant_id),
        ),
        refresh_token=create_refresh_token(
            subject=str(admin.id),
            role="tenant_admin",
            tenant_id=str(admin.tenant_id),
        ),
        admin=TenantAdminReadSchema.model_validate(admin),
    )
