from app.shared.exceptions import UnauthorizedException, ValidationException


class InvalidOtpException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__("The verification code is invalid or has expired.")


class OtpMaxAttemptsException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__(
            "Too many failed attempts. Please request a new code and try again."
        )


class OtpExpiredException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__("The verification code has expired. Please request a new one.")


class InvalidRefreshTokenException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Invalid or expired refresh token.")


class InvalidPhoneNumberException(ValidationException):
    def __init__(self) -> None:
        super().__init__("The phone number format is not valid.")
