from app.shared.exceptions import BigBossException


class InvalidCredentialsException(BigBossException):
    status_code = 401
    error_type = "invalid-credentials"
    title = "Credenciales inválidas"
    detail = "El correo o la contraseña son incorrectos."


class TenantAdminInactiveException(BigBossException):
    status_code = 403
    error_type = "tenant-admin-inactive"
    title = "Cuenta inactiva"
    detail = "Esta cuenta de administrador ha sido desactivada."
