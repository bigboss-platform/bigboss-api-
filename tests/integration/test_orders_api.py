from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.modules.end_users.models import EndUser
from app.modules.menus.models import Menu, MenuItem, MenuSection
from app.modules.orders.models import Order
from app.modules.tenants.models import Tenant, TenantSettings
from app.shared.enums import DeliveryType, OrderStatus, PaymentStatus


async def _seed_fixtures(session: AsyncSession) -> tuple[str, str, str, str]:
    tenant_slug = f"orders-test-{uuid4().hex[:8]}"
    tenant = Tenant(id=str(uuid4()), slug=tenant_slug, product="fastfood")
    session.add(tenant)
    await session.flush()

    tenant_settings = TenantSettings(
        id=str(uuid4()),
        tenant_id=tenant.id,
        business_lat=4.711,
        business_lng=-74.072,
        max_delivery_radius_km=10.0,
    )
    session.add(tenant_settings)

    menu = Menu(id=str(uuid4()), tenant_id=tenant.id)
    session.add(menu)
    await session.flush()

    section = MenuSection(
        id=str(uuid4()), menu_id=menu.id, name="Main", sort_order=1
    )
    session.add(section)
    await session.flush()

    item = MenuItem(
        id=str(uuid4()),
        section_id=section.id,
        name="Burger",
        price=8.50,
        sort_order=1,
        is_available=True,
    )
    session.add(item)

    end_user = EndUser(id=str(uuid4()), phone_number=f"+57{uuid4().int % 10**9:09d}", name="")
    session.add(end_user)
    await session.flush()

    return tenant_slug, tenant.id, item.id, end_user.id


@pytest.mark.asyncio
async def test_create_order_returns_201(
    integration_client: tuple[AsyncClient, AsyncSession],
) -> None:
    client, session = integration_client
    tenant_slug, tenant_id, item_id, end_user_id = await _seed_fixtures(session)

    token = create_access_token(subject=end_user_id, role="end_user", tenant_id=tenant_id)
    response = await client.post(
        f"/api/v1/tenants/{tenant_slug}/orders",
        json={
            "items": [{"menu_item_id": item_id, "quantity": 2}],
            "delivery_type": "pickup",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert len(data["items"]) == 1
    assert data["subtotal"] == pytest.approx(17.0)


@pytest.mark.asyncio
async def test_get_active_order_returns_order(
    integration_client: tuple[AsyncClient, AsyncSession],
) -> None:
    client, session = integration_client
    tenant_slug, tenant_id, item_id, end_user_id = await _seed_fixtures(session)

    order = Order(
        id=str(uuid4()),
        tenant_id=tenant_id,
        end_user_id=end_user_id,
        status=OrderStatus.PENDING,
        delivery_type=DeliveryType.PICKUP,
        delivery_address="",
        delivery_lat=0.0,
        delivery_lng=0.0,
        delivery_cost=0.0,
        subtotal=8.50,
        total=8.50,
        notes="",
        payment_status=PaymentStatus.PENDING,
    )
    session.add(order)
    await session.flush()

    token = create_access_token(subject=end_user_id, role="end_user", tenant_id=tenant_id)
    response = await client.get(
        f"/api/v1/tenants/{tenant_slug}/orders/active",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_advance_order_status(
    integration_client: tuple[AsyncClient, AsyncSession],
) -> None:
    client, session = integration_client
    _, tenant_id, _, end_user_id = await _seed_fixtures(session)

    order = Order(
        id=str(uuid4()),
        tenant_id=tenant_id,
        end_user_id=end_user_id,
        status=OrderStatus.PENDING,
        delivery_type=DeliveryType.PICKUP,
        delivery_address="",
        delivery_lat=0.0,
        delivery_lng=0.0,
        delivery_cost=0.0,
        subtotal=8.50,
        total=8.50,
        notes="",
        payment_status=PaymentStatus.PENDING,
    )
    session.add(order)
    await session.flush()

    admin_id = str(uuid4())
    token = create_access_token(subject=admin_id, role="tenant_admin", tenant_id=tenant_id)
    response = await client.put(
        f"/api/v1/backoffice/orders/{order.id}/status",
        json={"status": "confirmed"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "confirmed"


@pytest.mark.asyncio
async def test_backoffice_orders_list_requires_auth(
    integration_client: tuple[AsyncClient, AsyncSession],
) -> None:
    client, _ = integration_client
    response = await client.get("/api/v1/backoffice/orders")
    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_dashboard_stats_requires_auth(
    integration_client: tuple[AsyncClient, AsyncSession],
) -> None:
    client, _ = integration_client
    response = await client.get("/api/v1/backoffice/dashboard/stats")
    assert response.status_code in (401, 403)
