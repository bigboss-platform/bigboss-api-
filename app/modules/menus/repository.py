from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.menus.models import Menu, MenuItem, MenuSection


class MenuRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_tenant_id(self, tenant_id: str) -> Menu | None:
        result = await self._session.execute(
            select(Menu)
            .options(
                selectinload(Menu.sections).selectinload(MenuSection.items)
            )
            .where(Menu.tenant_id == tenant_id, Menu.is_deleted == False)  # noqa: E712
        )
        return result.scalar_one_or_none()

    async def find_section_by_id(self, section_id: str) -> MenuSection | None:
        result = await self._session.execute(
            select(MenuSection).where(
                MenuSection.id == section_id,
                MenuSection.is_deleted == False,  # noqa: E712
            )
        )
        return result.scalar_one_or_none()

    async def find_item_by_id(self, item_id: str) -> MenuItem | None:
        result = await self._session.execute(
            select(MenuItem).where(
                MenuItem.id == item_id, MenuItem.is_deleted == False  # noqa: E712
            )
        )
        return result.scalar_one_or_none()

    async def save(self, entity: Menu | MenuSection | MenuItem) -> None:
        self._session.add(entity)
        await self._session.flush()
