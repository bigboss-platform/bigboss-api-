from pydantic import field_validator

from app.shared.base_schema import BigBossBaseSchema, BigBossReadSchema


class MenuItemReadSchema(BigBossReadSchema):
    section_id: str
    name: str
    description: str
    price: float
    photo_url: str
    sort_order: int
    is_available: bool


class MenuItemCreateSchema(BigBossBaseSchema):
    name: str
    description: str = ""
    price: float
    photo_url: str = ""
    sort_order: int = 0

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("price must be greater than zero")
        return value


class MenuItemUpdateSchema(BigBossBaseSchema):
    name: str = ""
    description: str = ""
    price: float = 0.0
    photo_url: str = ""
    sort_order: int = 0
    is_available: bool = True


class MenuSectionReadSchema(BigBossReadSchema):
    menu_id: str
    name: str
    sort_order: int
    is_active: bool
    items: list[MenuItemReadSchema] = []


class MenuSectionCreateSchema(BigBossBaseSchema):
    name: str
    sort_order: int = 0


class MenuReadSchema(BigBossReadSchema):
    tenant_id: str
    is_active: bool
    sections: list[MenuSectionReadSchema] = []
