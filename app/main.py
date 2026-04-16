from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.middleware import TenantMiddleware
from app.modules.auth.router import router as auth_router
from app.modules.end_users.router import router as end_users_router
from app.modules.menus.router import router as menus_router
from app.modules.orders.router import router as orders_router
from app.modules.tenant_admins.router import router as tenant_admins_router
from app.modules.tenants.router import router as tenants_router

app = FastAPI(
    title="BigBoss API",
    version="0.1.0",
    docs_url="/docs" if settings.app_debug else None,
    redoc_url="/redoc" if settings.app_debug else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.app_debug else settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TenantMiddleware)

register_exception_handlers(app)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(tenants_router, prefix="/api/v1")
app.include_router(end_users_router, prefix="/api/v1")
app.include_router(menus_router, prefix="/api/v1")
app.include_router(orders_router, prefix="/api/v1")
app.include_router(tenant_admins_router, prefix="/api/v1")


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
