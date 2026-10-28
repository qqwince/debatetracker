from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    DB_HOST: str = "127.0.0.1"
    DB_PORT: str = "5432"
    DB_USER_NAME: str = "postgres"
    DB_NAME: str = "debatetracker"
    DB_PASSWORD: str = "mockPassword"

    # REDIS
    REDIS_HOST: str = "redis"
    REDIS_PORT: str = "6379"
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_JWT_SECONDS: int = 900
    CACHE_TTL_REFRESH_TOKEN_SECONDS: int = 3600
    CACHE_TTL_GAME_SECONDS: int = 2400

    # JWT
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"

    model_config = ConfigDict(env_file=".env")


settings = Settings()
