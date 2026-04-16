from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "local"
    app_secret_key: str = ""
    app_debug: bool = False
    allowed_origins: list[str] = []

    database_url: str = ""
    test_database_url: str = ""

    redis_url: str = ""

    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7

    smtp_host: str = "localhost"
    smtp_port: int = 1025
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from: str = "noreply@bigboss.io"

    otp_expire_seconds: int = 60
    otp_max_attempts: int = 3
    otp_test_phone: str = ""
    otp_test_code: str = ""


settings = Settings()
