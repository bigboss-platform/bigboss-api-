from app.shared.base_schema import BigBossBaseSchema, BigBossReadSchema


class TenantAdminLoginSchema(BigBossBaseSchema):
    email: str
    password: str


class TenantAdminReadSchema(BigBossReadSchema):
    tenant_id: str
    email: str
    name: str
    is_active: bool


class TenantAdminTokenSchema(BigBossBaseSchema):
    access_token: str
    refresh_token: str
    admin: TenantAdminReadSchema
