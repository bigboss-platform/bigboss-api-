from app.shared.exceptions import BigBossException


class InvalidCredentialsException(BigBossException):
    def __init__(self) -> None:
        super().__init__(
            status_code=401,
            error_type="invalid_credentials",
            title="Credenciales inválidas",
            detail="El correo o la contraseña son incorrectos.",
        )


class TenantAdminInactiveException(BigBossException):
    def __init__(self) -> None:
        super().__init__(
            status_code=403,
            error_type="tenant_admin_inactive",
            title="Cuenta inactiva",
            detail="Esta cuenta de administrador ha sido desactivada.",
        )
