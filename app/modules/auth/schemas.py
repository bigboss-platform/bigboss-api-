from pydantic import field_validator

from app.shared.base_schema import BigBossBaseSchema


class OtpRequestSchema(BigBossBaseSchema):
    phone_number: str
    tenant_id: str

    @field_validator("phone_number")
    @classmethod
    def phone_number_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("phone_number must not be empty")
        return value.strip()


class OtpVerifySchema(BigBossBaseSchema):
    phone_number: str
    code: str
    tenant_id: str


class TokenPairSchema(BigBossBaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshSchema(BigBossBaseSchema):
    refresh_token: str
