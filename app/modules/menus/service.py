from uuid import uuid4

from app.modules.menus.exceptions import (
    MenuItemNotFoundException,
    MenuNotFoundException,
    MenuSectionNotFoundException,
)
from app.modules.menus.models import Menu, MenuItem, MenuSection
from app.modules.menus.repository import MenuRepository
from app.modules.menus.schemas import (
    MenuItemCreateSchema,
    MenuItemReadSchema,
    MenuItemUpdateSchema,
    MenuReadSchema,
    MenuSectionCreateSchema,
    MenuSectionReadSchema,
    MenuSectionUpdateSchema,
)


class MenuService:
    def __init__(self, repository: MenuRepository) -> None:
        self._repository = repository

    async def get_menu_by_tenant_id(self, tenant_id: str) -> MenuReadSchema:
        menu = await self._repository.find_by_tenant_id(tenant_id)
        if menu is None:
            raise MenuNotFoundException(tenant_id)
        return self._to_end_user_schema(menu)

    async def get_menu_for_backoffice(self, tenant_id: str) -> MenuReadSchema:
        menu = await self._repository.find_by_tenant_id(tenant_id)
        if menu is None:
            raise MenuNotFoundException(tenant_id)
        return self._to_backoffice_schema(menu)

    async def get_item_by_id(self, item_id: str) -> MenuItemReadSchema:
        item = await self._repository.find_item_by_id(item_id)
        if item is None:
            raise MenuItemNotFoundException(item_id)
        return MenuItemReadSchema.model_validate(item)

    async def create_section(
        self, tenant_id: str, payload: MenuSectionCreateSchema
    ) -> MenuSectionReadSchema:
        menu = await self._repository.find_by_tenant_id(tenant_id)
        if menu is None:
            raise MenuNotFoundException(tenant_id)
        section = MenuSection(
            id=str(uuid4()),
            menu_id=menu.id,
            name=payload.name,
            sort_order=payload.sort_order,
        )
        await self._repository.save(section)
        return MenuSectionReadSchema(
            id=section.id,
            created_at=section.created_at,
            menu_id=section.menu_id,
            name=section.name,
            sort_order=section.sort_order,
            is_active=section.is_active,
            items=[],
        )

    async def update_section(
        self, section_id: str, payload: MenuSectionUpdateSchema
    ) -> MenuSectionReadSchema:
        section = await self._repository.find_section_by_id(section_id)
        if section is None:
            raise MenuSectionNotFoundException(section_id)
        if payload.name:
            section.name = payload.name
        section.sort_order = payload.sort_order
        section.is_active = payload.is_active
        await self._repository.save(section)
        updated = await self._repository.find_section_by_id(section_id)
        return MenuSectionReadSchema.model_validate(updated)

    async def delete_section(self, section_id: str) -> None:
        section = await self._repository.find_section_by_id(section_id)
        if section is None:
            raise MenuSectionNotFoundException(section_id)
        section.is_deleted = True
        await self._repository.save(section)

    async def create_item(
        self, section_id: str, payload: MenuItemCreateSchema
    ) -> MenuItemReadSchema:
        section = await self._repository.find_section_by_id(section_id)
        if section is None:
            raise MenuSectionNotFoundException(section_id)
        item = MenuItem(
            id=str(uuid4()),
            section_id=section_id,
            name=payload.name,
            description=payload.description,
            price=payload.price,
            photo_url=payload.photo_url,
            sort_order=payload.sort_order,
        )
        await self._repository.save(item)
        return MenuItemReadSchema.model_validate(item)

    async def update_item(
        self, item_id: str, payload: MenuItemUpdateSchema
    ) -> MenuItemReadSchema:
        item = await self._repository.find_item_by_id(item_id)
        if item is None:
            raise MenuItemNotFoundException(item_id)
        if payload.name:
            item.name = payload.name
        if payload.description:
            item.description = payload.description
        if payload.price > 0:
            item.price = payload.price
        if payload.photo_url:
            item.photo_url = payload.photo_url
        item.sort_order = payload.sort_order
        item.is_available = payload.is_available
        await self._repository.save(item)
        return MenuItemReadSchema.model_validate(item)

    async def delete_item(self, item_id: str) -> None:
        item = await self._repository.find_item_by_id(item_id)
        if item is None:
            raise MenuItemNotFoundException(item_id)
        item.is_deleted = True
        await self._repository.save(item)

    async def update_item_photo(self, item_id: str, photo_url: str) -> MenuItemReadSchema:
        item = await self._repository.find_item_by_id(item_id)
        if item is None:
            raise MenuItemNotFoundException(item_id)
        item.photo_url = photo_url
        await self._repository.save(item)
        return MenuItemReadSchema.model_validate(item)

    def _to_end_user_schema(self, menu: Menu) -> MenuReadSchema:
        sections = []
        for section in sorted(
            [s for s in menu.sections if not s.is_deleted and s.is_active],
            key=lambda s: s.sort_order,
        ):
            items = [
                MenuItemReadSchema.model_validate(i)
                for i in sorted(
                    [i for i in section.items if not i.is_deleted and i.is_available],
                    key=lambda i: i.sort_order,
                )
            ]
            sections.append(
                MenuSectionReadSchema(
                    id=section.id,
                    created_at=section.created_at,
                    menu_id=section.menu_id,
                    name=section.name,
                    sort_order=section.sort_order,
                    is_active=section.is_active,
                    items=items,
                )
            )
        return MenuReadSchema(
            id=menu.id,
            created_at=menu.created_at,
            tenant_id=menu.tenant_id,
            is_active=menu.is_active,
            sections=sections,
        )

    def _to_backoffice_schema(self, menu: Menu) -> MenuReadSchema:
        sections = []
        for section in sorted(
            [s for s in menu.sections if not s.is_deleted],
            key=lambda s: s.sort_order,
        ):
            items = [
                MenuItemReadSchema.model_validate(i)
                for i in sorted(
                    [i for i in section.items if not i.is_deleted],
                    key=lambda i: i.sort_order,
                )
            ]
            sections.append(
                MenuSectionReadSchema(
                    id=section.id,
                    created_at=section.created_at,
                    menu_id=section.menu_id,
                    name=section.name,
                    sort_order=section.sort_order,
                    is_active=section.is_active,
                    items=items,
                )
            )
        return MenuReadSchema(
            id=menu.id,
            created_at=menu.created_at,
            tenant_id=menu.tenant_id,
            is_active=menu.is_active,
            sections=sections,
        )
