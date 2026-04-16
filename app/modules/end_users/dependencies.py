from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.end_users.repository import EndUserRepository
from app.modules.end_users.service import EndUserService


def get_end_user_repository(
    session: AsyncSession = Depends(get_db_session),
) -> EndUserRepository:
    return EndUserRepository(session=session)


def get_end_user_service(
    repository: EndUserRepository = Depends(get_end_user_repository),
) -> EndUserService:
    return EndUserService(repository=repository)
