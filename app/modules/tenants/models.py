from sqlalchemy import Boolean, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base_model import TimestampedBase


class Tenant(TimestampedBase):
    __tablename__ = "tenants"
    __table_args__ = {"schema": "public"}

    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    product: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class TenantTheme(TimestampedBase):
    __tablename__ = "tenant_themes"
    __table_args__ = {"schema": "public"}

    tenant_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    primary_color: Mapped[str] = mapped_column(String(7), default="#000000")
    primary_color_hover: Mapped[str] = mapped_column(String(7), default="#333333")
    secondary_color: Mapped[str] = mapped_column(String(7), default="#ffffff")
    background_color: Mapped[str] = mapped_column(String(7), default="#ffffff")
    surface_color: Mapped[str] = mapped_column(String(7), default="#f5f5f5")
    text_primary_color: Mapped[str] = mapped_column(String(7), default="#212121")
    text_secondary_color: Mapped[str] = mapped_column(String(7), default="#757575")
    font_family_url: Mapped[str] = mapped_column(Text, default="")
    font_family_name: Mapped[str] = mapped_column(String(100), default="system-ui")
    logo_url: Mapped[str] = mapped_column(Text, default="")
    favicon_url: Mapped[str] = mapped_column(Text, default="")
    primary_button_text_color: Mapped[str] = mapped_column(String(7), default="#ffffff")
    loading_screen_background_color: Mapped[str] = mapped_column(String(7), default="#000000")


class TenantSettings(TimestampedBase):
    __tablename__ = "tenant_settings"
    __table_args__ = {"schema": "public"}

    tenant_id: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    business_name: Mapped[str] = mapped_column(String(200), default="")
    business_address: Mapped[str] = mapped_column(Text, default="")
    business_lat: Mapped[float] = mapped_column(Numeric(10, 7), default=0.0)
    business_lng: Mapped[float] = mapped_column(Numeric(10, 7), default=0.0)
    whatsapp_number: Mapped[str] = mapped_column(String(20), default="")
    whatsapp_message_template: Mapped[str] = mapped_column(Text, default="")
    max_delivery_radius_km: Mapped[float] = mapped_column(Numeric(5, 2), default=5.0)
    instagram_url: Mapped[str] = mapped_column(Text, default="")
    facebook_url: Mapped[str] = mapped_column(Text, default="")
    tiktok_url: Mapped[str] = mapped_column(Text, default="")
    twitter_url: Mapped[str] = mapped_column(Text, default="")
    payment_instructions: Mapped[str] = mapped_column(Text, default="El staff coordinará el pago.")
