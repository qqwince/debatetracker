from typing import AsyncGenerator

from httpx import ASGITransport, AsyncClient
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth import blacklist_token
from app.database import Base
from app.dependency import get_db
from app.repository.users import create_user
from main import app

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


@pytest_asyncio.fixture()
async def Client():
    yield TestClient(app)


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
async def authorized_client(db_session: AsyncSession):
    jwt_token = (await create_user(db=db_session, login="mock_user", password="mock_password"))["access_token"]
    await db_session.commit()
    headers = {"Authorization": f"Bearer {jwt_token}"}
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", headers=headers) as client:
        try:
            yield client
        finally:
            blacklist_token(jwt_token)