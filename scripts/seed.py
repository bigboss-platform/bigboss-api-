"""Seed script — creates demo tenant with FastFood demo data. Idempotent."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings
from app.modules.menus.models import Menu, MenuItem, MenuSection
from app.modules.tenant_admins.models import TenantAdmin
from app.modules.tenants.models import Tenant, TenantSettings, TenantTheme

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

TENANT_SLUG = "demo-fastfood"
ADMIN_EMAIL = "admin@demo-fastfood.com"
ADMIN_PASSWORD = "admin1234"


async def seed() -> None:
    engine = create_async_engine(settings.database_url, echo=False)
    factory = async_sessionmaker(engine, expire_on_commit=False)

    async with factory() as session:
        existing = (
            await session.execute(
                select(Tenant).where(Tenant.slug == TENANT_SLUG)
            )
        ).scalar_one_or_none()

        if existing:
            print(f"Tenant '{TENANT_SLUG}' already exists — skipping.")
            await engine.dispose()
            return

        tenant = Tenant(slug=TENANT_SLUG, product="fastfood", is_active=True)
        session.add(tenant)
        await session.flush()

        session.add(
            TenantTheme(
                tenant_id=tenant.id,
                primary_color="#E63946",
                primary_color_hover="#c1121f",
                secondary_color="#F1FAEE",
                background_color="#F1FAEE",
                surface_color="#ffffff",
                text_primary_color="#1d3557",
                text_secondary_color="#457b9d",
                font_family_url=(
                    "https://fonts.googleapis.com/css2"
                    "?family=Inter:wght@400;500;600;700&display=swap"
                ),
                font_family_name="Inter",
                logo_url="",
                favicon_url="",
                primary_button_text_color="#ffffff",
                loading_screen_background_color="#E63946",
            )
        )

        session.add(
            TenantSettings(
                tenant_id=tenant.id,
                business_name="Demo FastFood",
                business_address="Calle 123 #45-67, Bogotá",
                business_lat=4.7110,
                business_lng=-74.0721,
                whatsapp_number="+573001234567",
                whatsapp_message_template="Hola, acabo de realizar mi pedido #{order_id}",
                max_delivery_radius_km=5.0,
                payment_instructions="Paga al recibir tu pedido en efectivo o transferencia.",
            )
        )

        session.add(
            TenantAdmin(
                tenant_id=tenant.id,
                email=ADMIN_EMAIL,
                password_hash=_pwd.hash(ADMIN_PASSWORD),
                name="Demo Admin",
                is_active=True,
            )
        )

        menu = Menu(tenant_id=tenant.id, is_active=True)
        session.add(menu)

        hamburguesas = MenuSection(menu_id=menu.id, name="Hamburguesas", sort_order=1)
        bebidas = MenuSection(menu_id=menu.id, name="Bebidas", sort_order=2)
        session.add(hamburguesas)
        session.add(bebidas)

        burger_items = [
            ("Clásica", "Carne de res, lechuga, tomate y salsa especial", 18000, 1),
            ("BBQ Crispy", "Pollo crujiente, cheddar, cebolla caramelizada y BBQ", 22000, 2),
            ("Doble Smash", "Doble carne aplastada, queso americano y pepinillos", 26000, 3),
            ("Veggie Deluxe", "Medallón de garbanzo, aguacate, rúcula y mostaza dijon", 20000, 4),
        ]
        for name, desc, price, order in burger_items:
            session.add(
                MenuItem(
                    section_id=hamburguesas.id,
                    name=name,
                    description=desc,
                    price=price,
                    sort_order=order,
                    is_available=True,
                )
            )

        drink_items = [
            ("Limonada de Coco", "Limonada natural con leche de coco", 8000, 1),
            ("Gaseosa", "Coca-Cola, Sprite o Manzana — 400ml", 5000, 2),
        ]
        for name, desc, price, order in drink_items:
            session.add(
                MenuItem(
                    section_id=bebidas.id,
                    name=name,
                    description=desc,
                    price=price,
                    sort_order=order,
                    is_available=True,
                )
            )

        await session.commit()
        print(f"✓ Tenant '{TENANT_SLUG}' seeded (id={tenant.id})")
        print(f"  Admin: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
