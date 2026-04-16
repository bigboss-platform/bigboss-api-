from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.menus.dependencies import get_menu_service
from app.modules.menus.service import MenuService
from app.modules.orders.repository import OrderRepository
from app.modules.orders.service import OrderService
from app.modules.tenants.public import TenantService, get_tenant_service


def get_order_repository(
    session: AsyncSession = Depends(get_db_session),
) -> OrderRepository:
    return OrderRepository(session=session)


def get_order_service(
    order_repository: OrderRepository = Depends(get_order_repository),
    menu_service: MenuService = Depends(get_menu_service),
    tenant_service: TenantService = Depends(get_tenant_service),
) -> OrderService:
    return OrderService(
        order_repository=order_repository,
        menu_service=menu_service,
        tenant_service=tenant_service,
    )
