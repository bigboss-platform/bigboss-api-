from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.security import decode_token


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: object) -> Response:
        tenant_id = self._resolve_tenant_id(request)
        request.state.tenant_id = tenant_id
        return await call_next(request)  # type: ignore[operator]

    def _resolve_tenant_id(self, request: Request) -> str:
        authorization_header = request.headers.get("Authorization", "")
        if authorization_header.startswith("Bearer "):
            token = authorization_header.removeprefix("Bearer ")
            payload = decode_token(token)
            if payload:
                return payload.get("tenant_id", "")

        return request.headers.get("X-Tenant-Slug", "")
