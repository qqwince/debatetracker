from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    DB_HOST: str = "127.0.0.1"
    DB_PORT: str = "5432"
    DB_USER_NAME: str = "postgres"
    DB_NAME: str = "debatetracker"
    DB_PASSWORD: str

    # REDIS
    REDIS_HOST: str = "redis"
    REDIS_PORT: str = "6379"
    REDIS_URL: str = "redis://localhost:6379/0"
    cache_ttl_seconds: int = 3600
    cache_tasks_key: str = "cache:tasks_list"

    #JWT
    JWT_SECRET_KEY: str = "my-secret-key"
    ALGORITHM: str = "HS256"
    
    
    model_config = ConfigDict(env_file=".env")


settings = Settings()
