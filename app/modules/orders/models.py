from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base_model import TimestampedBase
from app.shared.enums import DeliveryType, OrderStatus, PaymentStatus


class Order(TimestampedBase):
    __tablename__ = "orders"

    tenant_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    end_user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default=OrderStatus.PENDING, nullable=False)
    delivery_type: Mapped[str] = mapped_column(String(20), nullable=False)
    delivery_address: Mapped[str] = mapped_column(Text, default="")
    delivery_lat: Mapped[float] = mapped_column(Numeric(10, 7), default=0.0)
    delivery_lng: Mapped[float] = mapped_column(Numeric(10, 7), default=0.0)
    delivery_cost: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    subtotal: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    notes: Mapped[str] = mapped_column(Text, default="")
    payment_status: Mapped[str] = mapped_column(
        String(50), default=PaymentStatus.PENDING, nullable=False
    )
    payment_method: Mapped[str] = mapped_column(String(200), default="")
    payment_amount_received: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    payment_reference: Mapped[str] = mapped_column(String(200), default="")
    payment_notes: Mapped[str] = mapped_column(Text, default="")
    payment_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    payment_updated_by: Mapped[str] = mapped_column(String, default="")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")


class OrderItem(TimestampedBase):
    __tablename__ = "order_items"

    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"), nullable=False)
    menu_item_id: Mapped[str] = mapped_column(String, nullable=False)
    menu_item_name: Mapped[str] = mapped_column(String(200), nullable=False)
    menu_item_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    note: Mapped[str] = mapped_column(Text, default="")
    order: Mapped["Order"] = relationship(back_populates="items")
