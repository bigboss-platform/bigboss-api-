from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_token

bearer_scheme = HTTPBearer()


@dataclass
class EndUserContext:
    end_user_id: str
    tenant_id: str
    role: str = "end_user"


@dataclass
class TenantAdminContext:
    tenant_admin_id: str
    tenant_id: str
    role: str = "tenant_admin"


@dataclass
class PlatformAdminContext:
    platform_admin_id: str
    role: str = "platform_admin"


def _extract_token_payload(
    credentials: HTTPAuthorizationCredentials,
) -> dict[str, str]:
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )
    return payload


def require_end_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> EndUserContext:
    payload = _extract_token_payload(credentials)
    if payload.get("role") != "end_user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden.")
    return EndUserContext(
        end_user_id=payload["sub"],
        tenant_id=payload["tenant_id"],
    )


def require_tenant_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> TenantAdminContext:
    payload = _extract_token_payload(credentials)
    if payload.get("role") != "tenant_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden.")
    return TenantAdminContext(
        tenant_admin_id=payload["sub"],
        tenant_id=payload["tenant_id"],
    )


def require_platform_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> PlatformAdminContext:
    payload = _extract_token_payload(credentials)
    if payload.get("role") != "platform_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden.")
    return PlatformAdminContext(platform_admin_id=payload["sub"])
