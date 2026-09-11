from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.users import router as users_router
from app.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users_router, prefix="/api/v1", tags=["users"])