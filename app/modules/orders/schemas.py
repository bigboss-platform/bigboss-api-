from datetime import datetime

from pydantic import field_validator

from app.shared.base_schema import BigBossBaseSchema, BigBossReadSchema
from app.shared.enums import DeliveryType, OrderStatus, PaymentStatus


class OrderItemCreateSchema(BigBossBaseSchema):
    menu_item_id: str
    quantity: int
    note: str = ""

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("quantity must be greater than zero")
        return value


class OrderCreateSchema(BigBossBaseSchema):
    items: list[OrderItemCreateSchema]
    delivery_type: DeliveryType
    delivery_address: str = ""
    delivery_lat: float = 0.0
    delivery_lng: float = 0.0
    notes: str = ""

    @field_validator("items")
    @classmethod
    def items_must_not_be_empty(cls, value: list[OrderItemCreateSchema]) -> list[OrderItemCreateSchema]:
        if not value:
            raise ValueError("Order must contain at least one item")
        return value


class OrderItemReadSchema(BigBossReadSchema):
    menu_item_id: str
    menu_item_name: str
    menu_item_price: float
    quantity: int
    note: str


class OrderReadSchema(BigBossReadSchema):
    end_user_id: str
    status: OrderStatus
    delivery_type: DeliveryType
    delivery_address: str
    delivery_cost: float
    subtotal: float
    total: float
    notes: str
    payment_status: PaymentStatus
    items: list[OrderItemReadSchema] = []


class OrderStatusUpdateSchema(BigBossBaseSchema):
    status: OrderStatus


class OrderPaymentUpdateSchema(BigBossBaseSchema):
    payment_status: PaymentStatus = PaymentStatus.PENDING
    payment_method: str = ""
    payment_amount_received: float = 0.0
    payment_reference: str = ""
    payment_notes: str = ""


class DeliveryCalculateSchema(BigBossBaseSchema):
    delivery_lat: float
    delivery_lng: float


class DeliveryCostSchema(BigBossBaseSchema):
    distance_km: float
    cost: float
    is_within_range: bool


class OrderListResponseSchema(BigBossBaseSchema):
    data: list[OrderReadSchema] = []
    total: int
    page: int
    page_size: int


class DashboardStatsSchema(BigBossBaseSchema):
    orders_today: int
    revenue_today: float
    active_orders: int
    pending_payments: int
