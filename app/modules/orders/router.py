from fastapi import APIRouter, Depends, Query

from app.core.dependencies import EndUserContext, TenantAdminContext, require_end_user, require_tenant_admin
from app.modules.orders.dependencies import get_order_service
from app.modules.orders.schemas import (
    DashboardStatsSchema,
    DeliveryCalculateSchema,
    DeliveryCostSchema,
    OrderCreateSchema,
    OrderListResponseSchema,
    OrderPaymentUpdateSchema,
    OrderReadSchema,
    OrderStatusUpdateSchema,
)
from app.modules.orders.service import OrderService
from app.modules.tenants.public import TenantService, get_tenant_service

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


@router.post("/tenants/{tenant_slug}/delivery/calculate", response_model=DeliveryCostSchema)
async def calculate_delivery(
    tenant_slug: str,
    payload: DeliveryCalculateSchema,
    current_user: EndUserContext = Depends(require_end_user),
    service: OrderService = Depends(get_order_service),
    tenant_service: TenantService = Depends(get_tenant_service),
) -> DeliveryCostSchema:
    tenant_id = await tenant_service.resolve_tenant_id(tenant_slug)
    return await service.calculate_delivery(tenant_id=tenant_id, payload=payload)


@router.get("/backoffice/orders", response_model=OrderListResponseSchema)
async def list_orders(
    status: str = Query(default=""),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_admin: TenantAdminContext = Depends(require_tenant_admin),
    service: OrderService = Depends(get_order_service),
) -> OrderListResponseSchema:
    return await service.list_by_tenant(
        tenant_id=current_admin.tenant_id,
        status_filter=status,
        page=page,
        page_size=page_size,
    )


@router.get("/backoffice/orders/{order_id}", response_model=OrderReadSchema)
async def get_backoffice_order(
    order_id: str,
    current_admin: TenantAdminContext = Depends(require_tenant_admin),
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


@router.get("/backoffice/dashboard/stats", response_model=DashboardStatsSchema)
async def get_dashboard_stats(
    current_admin: TenantAdminContext = Depends(require_tenant_admin),
    service: OrderService = Depends(get_order_service),
) -> DashboardStatsSchema:
    return await service.get_dashboard_stats(current_admin.tenant_id)
