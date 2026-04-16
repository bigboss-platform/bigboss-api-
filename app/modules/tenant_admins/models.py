from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base_model import TimestampedBase


class TenantAdmin(TimestampedBase):
    __tablename__ = "tenant_admins"
    __table_args__ = {"schema": "public"}

    tenant_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("public.tenants.id"),
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
