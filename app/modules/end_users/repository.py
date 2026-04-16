from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.end_users.models import EndUser


class EndUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, end_user_id: str) -> EndUser | None:
        result = await self._session.execute(
            select(EndUser).where(
                EndUser.id == end_user_id, EndUser.is_deleted == False  # noqa: E712
            )
        )
        return result.scalar_one_or_none()

    async def find_by_phone_number(self, phone_number: str) -> EndUser | None:
        result = await self._session.execute(
            select(EndUser).where(
                EndUser.phone_number == phone_number,
                EndUser.is_deleted == False,  # noqa: E712
            )
        )
        return result.scalar_one_or_none()

    async def create(self, phone_number: str) -> EndUser:
        end_user = EndUser(
            id=str(uuid4()),
            phone_number=phone_number,
            name="",
            consent_accepted_at=datetime.now(timezone.utc),
        )
        self._session.add(end_user)
        await self._session.flush()
        return end_user

    async def update_last_seen(self, end_user: EndUser) -> None:
        end_user.last_seen_at = datetime.now(timezone.utc)
        await self._session.flush()

    async def save(self, end_user: EndUser) -> EndUser:
        self._session.add(end_user)
        await self._session.flush()
        await self._session.refresh(end_user)
        return end_user
