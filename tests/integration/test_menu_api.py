from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.menus.models import Menu, MenuItem, MenuSection
from app.modules.tenants.models import Tenant


async def _seed_tenant_and_menu(session: AsyncSession) -> tuple[str, str]:
    tenant_slug = f"menu-test-{uuid4().hex[:8]}"
    tenant = Tenant(id=str(uuid4()), slug=tenant_slug, product="fastfood")
    session.add(tenant)
    await session.flush()

    menu = Menu(id=str(uuid4()), tenant_id=tenant.id)
    session.add(menu)
    await session.flush()

    section = MenuSection(
        id=str(uuid4()),
        menu_id=menu.id,
        name="Burgers",
        sort_order=1,
        is_active=True,
    )
    session.add(section)
    await session.flush()

    session.add(
        MenuItem(
            id=str(uuid4()),
            section_id=section.id,
            name="Classic Burger",
            price=9.99,
            sort_order=1,
            is_available=True,
        )
    )
    session.add(
        MenuItem(
            id=str(uuid4()),
            section_id=section.id,
            name="Sold Out Burger",
            price=12.99,
            sort_order=2,
            is_available=False,
        )
    )
    await session.flush()

    return tenant_slug, tenant.id


@pytest.mark.asyncio
async def test_get_menu_returns_only_available_items(
    integration_client: tuple[AsyncClient, AsyncSession],
) -> None:
    client, session = integration_client
    tenant_slug, _ = await _seed_tenant_and_menu(session)

    response = await client.get(f"/api/v1/tenants/{tenant_slug}/menu")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "sections" in data
    assert len(data["sections"]) == 1
    section = data["sections"][0]
    assert section["name"] == "Burgers"
    assert len(section["items"]) == 1
    assert section["items"][0]["name"] == "Classic Burger"


@pytest.mark.asyncio
async def test_get_menu_unknown_slug_returns_404_rfc7807(
    integration_client: tuple[AsyncClient, AsyncSession],
) -> None:
    client, _ = integration_client
    response = await client.get("/api/v1/tenants/does-not-exist/menu")
    assert response.status_code == 404
    data = response.json()
    assert "type" in data
    assert "title" in data
    assert "status" in data
    assert data["status"] == 404


@pytest.mark.asyncio
async def test_backoffice_menu_requires_auth(
    integration_client: tuple[AsyncClient, AsyncSession],
) -> None:
    client, _ = integration_client
    response = await client.get("/api/v1/backoffice/menu")
    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_create_section_requires_auth(
    integration_client: tuple[AsyncClient, AsyncSession],
) -> None:
    client, _ = integration_client
    response = await client.post(
        "/api/v1/backoffice/menu/sections",
        json={"name": "Drinks", "sort_order": 1},
    )
    assert response.status_code in (401, 403)
