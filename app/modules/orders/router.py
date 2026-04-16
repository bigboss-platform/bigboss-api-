from fastapi import APIRouter, Depends

from app.core.dependencies import EndUserContext, TenantAdminContext, require_end_user, require_tenant_admin
from app.modules.orders.dependencies import get_order_service
from app.modules.orders.schemas import (
    OrderCreateSchema,
    OrderPaymentUpdateSchema,
    OrderReadSchema,
    OrderStatusUpdateSchema,
)
from app.modules.orders.service import OrderService

router = APIRouter(tags=["orders"])


@router.post("/tenants/{tenant_slug}/orders", response_model=OrderReadSchema, status_code=201)
async def create_order(
    tenant_slug: str,
    payload: OrderCreateSchema,
    current_user: EndUserContext = Depends(require_end_user),
    service: OrderService = Depends(get_order_service),
) -> OrderReadSchema:
    return await service.create_order(current_user.end_user_id, current_user.tenant_id, payload)


@router.get("/tenants/{tenant_slug}/orders/active", response_model=OrderReadSchema | None)
async def get_active_order(
    tenant_slug: str,
    current_user: EndUserContext = Depends(require_end_user),
    service: OrderService = Depends(get_order_service),
) -> OrderReadSchema | None:
    return await service.get_active_order(current_user.end_user_id)


@router.get("/tenants/{tenant_slug}/orders/{order_id}", response_model=OrderReadSchema)
async def get_order(
    tenant_slug: str,
    order_id: str,
    current_user: EndUserContext = Depends(require_end_user),
    service: OrderService = Depends(get_order_service),
) -> OrderReadSchema:
    return await service.get_by_id(order_id)


@router.put("/backoffice/orders/{order_id}/status", response_model=OrderReadSchema)
async def update_order_status(
    order_id: str,
    payload: OrderStatusUpdateSchema,
    current_admin: TenantAdminContext = Depends(require_tenant_admin),
    service: OrderService = Depends(get_order_service),
) -> OrderReadSchema:
    return await service.update_status(order_id, payload)


@router.patch("/backoffice/orders/{order_id}/payment", response_model=OrderReadSchema)
async def update_order_payment(
    order_id: str,
    payload: OrderPaymentUpdateSchema,
    current_admin: TenantAdminContext = Depends(require_tenant_admin),
    service: OrderService = Depends(get_order_service),
) -> OrderReadSchema:
    return await service.update_payment(order_id, payload, current_admin.tenant_admin_id)
