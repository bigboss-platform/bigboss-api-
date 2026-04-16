import pytest
from unittest.mock import AsyncMock, patch

from app.modules.auth.exceptions import InvalidOtpException, OtpExpiredException
from app.modules.auth.schemas import OtpRequestSchema, OtpVerifySchema
from app.modules.auth.service import AuthService
from app.core.security import hash_otp_code
from datetime import datetime, timedelta, timezone


def build_otp_fixture(code: str = "123456", expired: bool = False) -> AsyncMock:
    otp = AsyncMock()
    otp.code_hash = hash_otp_code(code)
    otp.attempt_count = 0
    otp.expires_at = (
        datetime.now(timezone.utc) - timedelta(seconds=1)
        if expired
        else datetime.now(timezone.utc) + timedelta(seconds=60)
    )
    return otp


@pytest.mark.asyncio
async def test_request_otp_creates_otp_verification() -> None:
    mock_auth_repo = AsyncMock()
    mock_end_user_service = AsyncMock()
    service = AuthService(
        auth_repository=mock_auth_repo,
        end_user_service=mock_end_user_service,
    )

    result = await service.request_otp(
        OtpRequestSchema(phone_number="+573001234567", tenant_id="tenant-001")
    )

    assert result["expires_in_seconds"] > 0
    mock_auth_repo.create_otp_verification.assert_called_once()


@pytest.mark.asyncio
async def test_verify_otp_when_code_is_correct_returns_token_pair() -> None:
    mock_auth_repo = AsyncMock()
    mock_auth_repo.find_latest_active_otp.return_value = build_otp_fixture("123456")
    mock_end_user_service = AsyncMock()
    mock_end_user_service.find_or_create_by_phone.return_value = AsyncMock(id="user-001")
    service = AuthService(
        auth_repository=mock_auth_repo,
        end_user_service=mock_end_user_service,
    )

    result = await service.verify_otp(
        OtpVerifySchema(
            phone_number="+573001234567", code="123456", tenant_id="tenant-001"
        )
    )

    assert result.access_token != ""
    assert result.refresh_token != ""


@pytest.mark.asyncio
async def test_verify_otp_when_no_active_otp_raises_expired_exception() -> None:
    mock_auth_repo = AsyncMock()
    mock_auth_repo.find_latest_active_otp.return_value = None
    service = AuthService(
        auth_repository=mock_auth_repo,
        end_user_service=AsyncMock(),
    )

    with pytest.raises(OtpExpiredException):
        await service.verify_otp(
            OtpVerifySchema(
                phone_number="+573001234567", code="000000", tenant_id="tenant-001"
            )
        )


@pytest.mark.asyncio
async def test_verify_otp_when_code_is_wrong_raises_invalid_otp_exception() -> None:
    mock_auth_repo = AsyncMock()
    mock_auth_repo.find_latest_active_otp.return_value = build_otp_fixture("123456")
    service = AuthService(
        auth_repository=mock_auth_repo,
        end_user_service=AsyncMock(),
    )

    with pytest.raises(InvalidOtpException):
        await service.verify_otp(
            OtpVerifySchema(
                phone_number="+573001234567", code="999999", tenant_id="tenant-001"
            )
        )
