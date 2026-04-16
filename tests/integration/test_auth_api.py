from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings


@pytest.mark.asyncio
async def test_request_otp_returns_200(
    integration_client: tuple[AsyncClient, AsyncSession],
) -> None:
    client, _ = integration_client
    response = await client.post(
        "/api/v1/auth/otp/request",
        json={"phone_number": "+1234567890", "tenant_id": "tenant-test"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "expires_in_seconds" in data["data"]


@pytest.mark.asyncio
async def test_verify_otp_with_staging_bypass_returns_tokens(
    integration_client: tuple[AsyncClient, AsyncSession],
) -> None:
    client, _ = integration_client
    test_phone = settings.otp_test_phone
    test_code = settings.otp_test_code
    if not test_phone or not test_code:
        pytest.skip("OTP_TEST_PHONE and OTP_TEST_CODE not configured")

    await client.post(
        "/api/v1/auth/otp/request",
        json={"phone_number": test_phone, "tenant_id": "tenant-test"},
    )
    response = await client.post(
        "/api/v1/auth/otp/verify",
        json={"phone_number": test_phone, "code": test_code, "tenant_id": "tenant-test"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_verify_otp_wrong_code_returns_401(
    integration_client: tuple[AsyncClient, AsyncSession],
) -> None:
    client, _ = integration_client
    await client.post(
        "/api/v1/auth/otp/request",
        json={"phone_number": "+9999999999", "tenant_id": "tenant-test"},
    )
    response = await client.post(
        "/api/v1/auth/otp/verify",
        json={"phone_number": "+9999999999", "code": "badcod", "tenant_id": "tenant-test"},
    )
    assert response.status_code == 401
    data = response.json()
    assert "type" in data
    assert "status" in data


@pytest.mark.asyncio
async def test_token_refresh_with_invalid_token_returns_401(
    integration_client: tuple[AsyncClient, AsyncSession],
) -> None:
    client, _ = integration_client
    response = await client.post(
        "/api/v1/auth/token/refresh",
        json={"refresh_token": "invalid.token.here"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_without_auth_returns_401_or_403(
    integration_client: tuple[AsyncClient, AsyncSession],
) -> None:
    client, _ = integration_client
    response = await client.get("/api/v1/end-users/me")
    assert response.status_code in (401, 403)
