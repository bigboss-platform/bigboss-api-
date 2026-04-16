from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import OtpVerification


class AuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_otp_verification(
        self, phone_number: str, code_hash: str, expires_at: datetime
    ) -> OtpVerification:
        otp = OtpVerification(
            id=str(uuid4()),
            phone_number=phone_number,
            code_hash=code_hash,
            expires_at=expires_at,
            is_used=False,
            attempt_count=0,
        )
        self._session.add(otp)
        await self._session.flush()
        return otp

    async def find_latest_active_otp(
        self, phone_number: str
    ) -> OtpVerification | None:
        result = await self._session.execute(
            select(OtpVerification)
            .where(
                OtpVerification.phone_number == phone_number,
                OtpVerification.is_used == False,  # noqa: E712
                OtpVerification.expires_at > datetime.now(timezone.utc),
            )
            .order_by(OtpVerification.expires_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def increment_attempt_count(self, otp: OtpVerification) -> None:
        otp.attempt_count += 1
        await self._session.flush()

    async def mark_otp_as_used(self, otp: OtpVerification) -> None:
        otp.is_used = True
        await self._session.flush()
