from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_otp_code,
    hash_otp_code,
)
from app.modules.auth.exceptions import (
    InvalidOtpException,
    InvalidRefreshTokenException,
    OtpExpiredException,
    OtpMaxAttemptsException,
)
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import OtpRequestSchema, OtpVerifySchema, TokenPairSchema, TokenRefreshSchema
from app.modules.end_users.public import EndUserService


class AuthService:
    def __init__(
        self,
        auth_repository: AuthRepository,
        end_user_service: EndUserService,
    ) -> None:
        self._auth_repository = auth_repository
        self._end_user_service = end_user_service

    async def request_otp(self, payload: OtpRequestSchema) -> dict[str, int]:
        code = self._resolve_otp_code(payload.phone_number)
        code_hash = hash_otp_code(code)
        expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=settings.otp_expire_seconds
        )
        await self._auth_repository.create_otp_verification(
            phone_number=payload.phone_number,
            code_hash=code_hash,
            expires_at=expires_at,
        )
        return {"expires_in_seconds": settings.otp_expire_seconds}

    async def verify_otp(self, payload: OtpVerifySchema) -> TokenPairSchema:
        otp = await self._auth_repository.find_latest_active_otp(payload.phone_number)

        if otp is None:
            raise OtpExpiredException()

        if otp.attempt_count >= settings.otp_max_attempts:
            raise OtpMaxAttemptsException()

        if otp.code_hash != hash_otp_code(payload.code):
            await self._auth_repository.increment_attempt_count(otp)
            raise InvalidOtpException()

        await self._auth_repository.mark_otp_as_used(otp)

        end_user = await self._end_user_service.find_or_create_by_phone(
            phone_number=payload.phone_number,
            tenant_id=payload.tenant_id,
        )

        return TokenPairSchema(
            access_token=create_access_token(
                subject=end_user.id,
                role="end_user",
                tenant_id=payload.tenant_id,
            ),
            refresh_token=create_refresh_token(
                subject=end_user.id,
                role="end_user",
                tenant_id=payload.tenant_id,
            ),
        )

    async def refresh_token(self, payload: TokenRefreshSchema) -> TokenPairSchema:
        token_data = decode_token(payload.refresh_token)
        if not token_data or token_data.get("type") != "refresh":
            raise InvalidRefreshTokenException()
        return TokenPairSchema(
            access_token=create_access_token(
                subject=token_data["sub"],
                role=token_data["role"],
                tenant_id=token_data["tenant_id"],
            ),
            refresh_token=create_refresh_token(
                subject=token_data["sub"],
                role=token_data["role"],
                tenant_id=token_data["tenant_id"],
            ),
        )

    def _resolve_otp_code(self, phone_number: str) -> str:
        is_staging_bypass_enabled = (
            settings.otp_test_phone != ""
            and settings.otp_test_code != ""
            and settings.app_env != "production"
        )
        if is_staging_bypass_enabled and phone_number == settings.otp_test_phone:
            return settings.otp_test_code
        return generate_otp_code()
