from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.users import router as users_router
from app.api.v1.games import router as games_router
from app.cache.cache import lifespan

app = FastAPI(title="Debate Tracker API", lifespan=lifespan)

app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(games_router, prefix="/api/v1", tags=["games"])
