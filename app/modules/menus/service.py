from app.modules.menus.exceptions import MenuItemNotFoundException, MenuNotFoundException
from app.modules.menus.repository import MenuRepository
from app.modules.menus.schemas import MenuItemReadSchema, MenuReadSchema


class MenuService:
    def __init__(self, repository: MenuRepository) -> None:
        self._repository = repository

    async def get_menu_by_tenant_id(self, tenant_id: str) -> MenuReadSchema:
        menu = await self._repository.find_by_tenant_id(tenant_id)
        if menu is None:
            raise MenuNotFoundException(tenant_id)
        return MenuReadSchema.model_validate(menu)

    async def get_item_by_id(self, item_id: str) -> MenuItemReadSchema:
        item = await self._repository.find_item_by_id(item_id)
        if item is None:
            raise MenuItemNotFoundException(item_id)
        return MenuItemReadSchema.model_validate(item)
