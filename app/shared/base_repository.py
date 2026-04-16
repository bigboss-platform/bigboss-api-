from typing import Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.base_model import TimestampedBase

ModelType = TypeVar("ModelType", bound=TimestampedBase)


class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, entity_id: str) -> ModelType | None:
        result = await self._session.execute(
            select(self.model).where(
                self.model.id == entity_id,
                self.model.is_deleted == False,  # noqa: E712
            )
        )
        return result.scalar_one_or_none()

    async def find_all(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[list[ModelType], int]:
        base_query = select(self.model).where(
            self.model.is_deleted == False  # noqa: E712
        )
        count_result = await self._session.execute(
            select(func.count()).select_from(base_query.subquery())
        )
        total = count_result.scalar_one()
        items_result = await self._session.execute(
            base_query.offset((page - 1) * page_size).limit(page_size)
        )
        return list(items_result.scalars().all()), total

    async def save(self, entity: ModelType) -> ModelType:
        self._session.add(entity)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity

    async def soft_delete(self, entity: ModelType) -> None:
        entity.is_deleted = True
        await self._session.flush()
