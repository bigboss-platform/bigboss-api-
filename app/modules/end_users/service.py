from app.modules.end_users.exceptions import EndUserNotFoundException
from app.modules.end_users.repository import EndUserRepository
from app.modules.end_users.schemas import EndUserReadSchema, EndUserUpdateSchema


class EndUserService:
    def __init__(self, repository: EndUserRepository) -> None:
        self._repository = repository

    async def find_or_create_by_phone(
        self, phone_number: str, tenant_id: str
    ) -> EndUserReadSchema:
        end_user = await self._repository.find_by_phone_number(phone_number)
        if end_user is None:
            end_user = await self._repository.create(phone_number=phone_number)
        else:
            await self._repository.update_last_seen(end_user)
        return EndUserReadSchema.model_validate(end_user)

    async def get_by_id(self, end_user_id: str) -> EndUserReadSchema:
        end_user = await self._repository.find_by_id(end_user_id)
        if end_user is None:
            raise EndUserNotFoundException(end_user_id)
        return EndUserReadSchema.model_validate(end_user)

    async def update(
        self, end_user_id: str, payload: EndUserUpdateSchema
    ) -> EndUserReadSchema:
        end_user = await self._repository.find_by_id(end_user_id)
        if end_user is None:
            raise EndUserNotFoundException(end_user_id)
        if payload.name:
            end_user.name = payload.name
        saved = await self._repository.save(end_user)
        return EndUserReadSchema.model_validate(saved)
