from typing import AsyncGenerator

import fakeredis
from httpx import ASGITransport, AsyncClient
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from requests import session
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.cache.cache import get_redis
from app.database import Base
from app.dependency import get_db
from app.repository.users import create_user
from main import app
import app.cache.cache as cache_module 

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db





@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture()
async def authorized_client(db_session: AsyncSession, redis):
    jwt_token = (await create_user(db=db_session, redis=redis, login="mock_user", password="mock_password"))["access_token"]
    await db_session.commit()
    headers = {"Authorization": f"Bearer {jwt_token}"}
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", headers=headers) as client:
            yield client


@pytest_asyncio.fixture
async def redis() -> AsyncGenerator[fakeredis.aioredis.FakeRedis, None]:
    fake = fakeredis.aioredis.FakeRedis(decode_responses=True)

    app.dependency_overrides[get_redis] = lambda: fake
    old_global = getattr(cache_module, "redis_client", None)
    cache_module.redis_client = fake
    app.redis_client = fake

    yield fake

    cache_module.redis_client = old_global
    app.redis_client = None
    app.dependency_overrides.pop(get_redis, None)
    await fake.aclose()

@pytest_asyncio.fixture
async def client(redis) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture()
def Client(redis):
    yield TestClient(app)
    