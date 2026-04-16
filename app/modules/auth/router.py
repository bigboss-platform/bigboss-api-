from fastapi import APIRouter, Depends

from app.modules.auth.dependencies import get_auth_service
from app.modules.auth.schemas import OtpRequestSchema, OtpVerifySchema, TokenPairSchema
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/otp/request", status_code=200)
async def request_otp(
    payload: OtpRequestSchema,
    service: AuthService = Depends(get_auth_service),
) -> dict[str, object]:
    result = await service.request_otp(payload)
    return {"data": result}


@router.post("/otp/verify", response_model=TokenPairSchema)
async def verify_otp(
    payload: OtpVerifySchema,
    service: AuthService = Depends(get_auth_service),
) -> TokenPairSchema:
    return await service.verify_otp(payload)
