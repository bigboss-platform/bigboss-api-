from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.orders.models import Order, OrderItem
from app.shared.enums import OrderStatus, PaymentStatus


class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, order_id: str) -> Order | None:
        result = await self._session.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id, Order.is_deleted == False)  # noqa: E712
        )
        return result.scalar_one_or_none()

    async def find_active_by_end_user(self, end_user_id: str) -> Order | None:
        active_statuses = [
            OrderStatus.PENDING,
            OrderStatus.CONFIRMED,
            OrderStatus.PREPARING,
            OrderStatus.READY,
        ]
        result = await self._session.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(
                Order.end_user_id == end_user_id,
                Order.status.in_(active_statuses),
                Order.is_deleted == False,  # noqa: E712
            )
            .order_by(Order.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def find_all_by_tenant(
        self,
        tenant_id: str,
        status_filter: str = "",
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Order], int]:
        base_query = select(Order).where(
            Order.tenant_id == tenant_id,
            Order.is_deleted == False,  # noqa: E712
        )
        if status_filter:
            base_query = base_query.where(Order.status == status_filter)
        base_query = base_query.order_by(Order.created_at.desc())
        count_result = await self._session.execute(
            select(func.count()).select_from(base_query.subquery())
        )
        total = count_result.scalar_one()
        items_result = await self._session.execute(
            base_query.options(selectinload(Order.items))
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(items_result.scalars().all()), total

    async def get_dashboard_stats(self, tenant_id: str) -> dict[str, object]:
        today_start = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        active_statuses = [
            OrderStatus.PENDING,
            OrderStatus.CONFIRMED,
            OrderStatus.PREPARING,
            OrderStatus.READY,
        ]
        orders_today_result = await self._session.execute(
            select(func.count(Order.id)).where(
                Order.tenant_id == tenant_id,
                Order.created_at >= today_start,
                Order.is_deleted == False,  # noqa: E712
            )
        )
        revenue_today_result = await self._session.execute(
            select(func.coalesce(func.sum(Order.total), 0.0)).where(
                Order.tenant_id == tenant_id,
                Order.created_at >= today_start,
                Order.payment_status == PaymentStatus.PAID,
                Order.is_deleted == False,  # noqa: E712
            )
        )
        active_orders_result = await self._session.execute(
            select(func.count(Order.id)).where(
                Order.tenant_id == tenant_id,
                Order.status.in_(active_statuses),
                Order.is_deleted == False,  # noqa: E712
            )
        )
        pending_payments_result = await self._session.execute(
            select(func.count(Order.id)).where(
                Order.tenant_id == tenant_id,
                Order.payment_status == PaymentStatus.PENDING,
                Order.is_deleted == False,  # noqa: E712
            )
        )
        return {
            "orders_today": orders_today_result.scalar_one(),
            "revenue_today": float(revenue_today_result.scalar_one()),
            "active_orders": active_orders_result.scalar_one(),
            "pending_payments": pending_payments_result.scalar_one(),
        }

    async def find_all_by_end_user(
        self, end_user_id: str, page: int = 1, page_size: int = 20
    ) -> tuple[list[Order], int]:
        base_query = (
            select(Order)
            .where(Order.end_user_id == end_user_id, Order.is_deleted == False)  # noqa: E712
            .order_by(Order.created_at.desc())
        )
        count_result = await self._session.execute(
            select(func.count()).select_from(base_query.subquery())
        )
        total = count_result.scalar_one()
        items_result = await self._session.execute(
            base_query.options(selectinload(Order.items))
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(items_result.scalars().all()), total

    async def create(self, order: Order) -> Order:
        self._session.add(order)
        await self._session.flush()
        return order

    async def save(self, order: Order) -> Order:
        self._session.add(order)
        await self._session.flush()
        await self._session.refresh(order)
        return order

    async def update_payment(
        self,
        order: Order,
        payment_status: str,
        payment_method: str,
        payment_amount_received: float,
        payment_reference: str,
        payment_notes: str,
        updated_by: str,
    ) -> Order:
        order.payment_status = payment_status
        order.payment_method = payment_method
        order.payment_amount_received = payment_amount_received
        order.payment_reference = payment_reference
        order.payment_notes = payment_notes
        order.payment_updated_by = updated_by
        order.payment_updated_at = datetime.now(timezone.utc)
        await self._session.flush()
        return order
