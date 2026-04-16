from app.shared.base_schema import BigBossBaseSchema, BigBossReadSchema


class EndUserReadSchema(BigBossReadSchema):
    phone_number: str
    name: str


class EndUserUpdateSchema(BigBossBaseSchema):
    name: str = ""
