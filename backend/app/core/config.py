from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application configuration, loaded from environment variables / .env.
    Never hard-code secrets here — only defaults safe for local dev fallbacks.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "ServiceOps"
    APP_ENV: str = "development"

    DATABASE_URL: str = "postgresql://serviceops:serviceops@localhost:5432/serviceops"

    JWT_SECRET: str = "change-me-in-env"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24

    NEXT_PUBLIC_API_URL: str = "http://localhost:8000"

    # Used only by the seed script — never hard-coded, always from env
    SEED_ADMIN_EMAIL: str = "admin@serviceops.local"
    SEED_ADMIN_PASSWORD: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
