from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BigBossBaseSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)


class BigBossReadSchema(BigBossBaseSchema):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    id: str
    created_at: datetime


class PaginatedResponseSchema(BigBossBaseSchema):
    total: int
    page: int
    page_size: int
