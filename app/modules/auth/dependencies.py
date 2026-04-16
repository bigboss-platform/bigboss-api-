from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.auth.repository import AuthRepository
from app.modules.auth.service import AuthService
from app.modules.end_users.public import EndUserService
from app.modules.end_users.dependencies import get_end_user_service


def get_auth_repository(
    session: AsyncSession = Depends(get_db_session),
) -> AuthRepository:
    return AuthRepository(session=session)


def get_auth_service(
    auth_repository: AuthRepository = Depends(get_auth_repository),
    end_user_service: EndUserService = Depends(get_end_user_service),
) -> AuthService:
    return AuthService(
        auth_repository=auth_repository,
        end_user_service=end_user_service,
    )
