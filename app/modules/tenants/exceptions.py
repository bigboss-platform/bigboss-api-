from app.shared.exceptions import NotFoundException


class TenantNotFoundException(NotFoundException):
    def __init__(self, tenant_slug: str) -> None:
        super().__init__(f"Tenant with slug '{tenant_slug}' does not exist.")


class TenantThemeNotFoundException(NotFoundException):
    def __init__(self, tenant_id: str) -> None:
        super().__init__(f"Theme for tenant '{tenant_id}' does not exist.")
