from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base_model import TimestampedBase


class Menu(TimestampedBase):
    __tablename__ = "menus"

    tenant_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sections: Mapped[list["MenuSection"]] = relationship(back_populates="menu")


class MenuSection(TimestampedBase):
    __tablename__ = "menu_sections"

    menu_id: Mapped[str] = mapped_column(ForeignKey("menus.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    menu: Mapped["Menu"] = relationship(back_populates="sections")
    items: Mapped[list["MenuItem"]] = relationship(back_populates="section")


class MenuItem(TimestampedBase):
    __tablename__ = "menu_items"

    section_id: Mapped[str] = mapped_column(ForeignKey("menu_sections.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    photo_url: Mapped[str] = mapped_column(Text, default="")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    section: Mapped["MenuSection"] = relationship(back_populates="items")
