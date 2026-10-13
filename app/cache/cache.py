from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from redis.asyncio import Redis

redis_client: Redis | None = None


async def get_redis() -> AsyncGenerator[Redis, None]:
    if redis_client is None:
        raise RuntimeError("Redis client is not initialized")
    yield redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client
    # Инициализация пула соединений при старте приложения
    # Если Redis работает в Docker-compose, используйте имя сервиса (например, host="redis")
    redis_client = Redis(host="redis", port=6379, db=0, decode_responses=True)

    yield

    # Закрытие соединений при завершении работы
    await redis_client.aclose()
