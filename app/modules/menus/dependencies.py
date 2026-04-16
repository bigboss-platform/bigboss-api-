from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.menus.repository import MenuRepository
from app.modules.menus.service import MenuService


def get_menu_repository(session: AsyncSession = Depends(get_db_session)) -> MenuRepository:
    return MenuRepository(session=session)


def get_menu_service(
    repository: MenuRepository = Depends(get_menu_repository),
) -> MenuService:
    return MenuService(repository=repository)
