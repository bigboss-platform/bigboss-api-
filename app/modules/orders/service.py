from uuid import uuid4

from app.modules.menus.public import MenuItemNotFoundException, MenuService
from app.modules.orders.exceptions import OrderAlreadyCancelledException, OrderNotFoundException
from app.modules.orders.models import Order, OrderItem
from app.modules.orders.repository import OrderRepository
from app.modules.orders.schemas import (
    DeliveryCalculateSchema,
    DeliveryCostSchema,
    OrderCreateSchema,
    OrderPaymentUpdateSchema,
    OrderReadSchema,
    OrderStatusUpdateSchema,
)
from app.shared.enums import OrderStatus
from app.shared.utils import calculate_haversine_distance_km


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        menu_service: MenuService,
    ) -> None:
        self._order_repository = order_repository
        self._menu_service = menu_service

    async def create_order(
        self, end_user_id: str, tenant_id: str, payload: OrderCreateSchema
    ) -> OrderReadSchema:
        subtotal = 0.0
        order_items: list[OrderItem] = []

        for cart_item in payload.items:
            menu_item = await self._menu_service.get_item_by_id(cart_item.menu_item_id)
            item_total = menu_item.price * cart_item.quantity
            subtotal += item_total
            order_items.append(
                OrderItem(
                    id=str(uuid4()),
                    order_id="",
                    menu_item_id=menu_item.id,
                    menu_item_name=menu_item.name,
                    menu_item_price=menu_item.price,
                    quantity=cart_item.quantity,
                    note=cart_item.note,
                )
            )

        order = Order(
            id=str(uuid4()),
            end_user_id=end_user_id,
            status=OrderStatus.PENDING,
            delivery_type=payload.delivery_type,
            delivery_address=payload.delivery_address,
            delivery_lat=payload.delivery_lat,
            delivery_lng=payload.delivery_lng,
            delivery_cost=0.0,
            subtotal=subtotal,
            total=subtotal,
            notes=payload.notes,
        )

        created_order = await self._order_repository.create(order)
        for item in order_items:
            item.order_id = created_order.id
            created_order.items.append(item)

        saved_order = await self._order_repository.save(created_order)
        return OrderReadSchema.model_validate(saved_order)

    async def get_by_id(self, order_id: str) -> OrderReadSchema:
        order = await self._order_repository.find_by_id(order_id)
        if order is None:
            raise OrderNotFoundException(order_id)
        return OrderReadSchema.model_validate(order)

    async def get_active_order(self, end_user_id: str) -> OrderReadSchema | None:
        order = await self._order_repository.find_active_by_end_user(end_user_id)
        if order is None:
            return None
        return OrderReadSchema.model_validate(order)

    async def update_status(
        self, order_id: str, payload: OrderStatusUpdateSchema
    ) -> OrderReadSchema:
        order = await self._order_repository.find_by_id(order_id)
        if order is None:
            raise OrderNotFoundException(order_id)
        if order.status == OrderStatus.CANCELLED:
            raise OrderAlreadyCancelledException(order_id)
        order.status = payload.status
        saved = await self._order_repository.save(order)
        return OrderReadSchema.model_validate(saved)

    async def update_payment(
        self, order_id: str, payload: OrderPaymentUpdateSchema, updated_by: str
    ) -> OrderReadSchema:
        order = await self._order_repository.find_by_id(order_id)
        if order is None:
            raise OrderNotFoundException(order_id)
        updated = await self._order_repository.update_payment(
            order=order,
            payment_status=payload.payment_status,
            payment_method=payload.payment_method,
            payment_amount_received=payload.payment_amount_received,
            payment_reference=payload.payment_reference,
            payment_notes=payload.payment_notes,
            updated_by=updated_by,
        )
        return OrderReadSchema.model_validate(updated)
