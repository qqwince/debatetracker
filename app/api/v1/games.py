
from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import get_redis
from app.dependency import get_current_user, get_db
from app.models import User
from app.schemas.games import (
    GameListParams,
    GamePaginationResponse,
    GameRequest,
    GameResponse,
    GameUpdate,
)
from app.service import games as games_service

router = APIRouter()


@router.post("/game", response_model=GameResponse)
async def create_game(
    payload: GameRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await games_service.create_game(db, payload, current_user)


@router.get("/game/{game_id}", response_model=GameResponse)
async def get_game_by_id(
    game_id: int,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user),
):
    return await games_service.get_game_by_id(db, redis, current_user, game_id)


@router.get("/game", response_model=GamePaginationResponse)
async def get_game_pagination(
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user),
    params: GameListParams = Depends(GameListParams),
):
    return await games_service.get_game_pagination(
        db, redis, current_user, params.limit, params.cursor
    )


@router.patch("/game", response_model=GameResponse)
async def edit_game(
    payload: GameUpdate,
    game_id: int,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user),
):
    return await games_service.edit_game(db, redis, game_id, payload, current_user)


@router.delete("/game")
async def delete_game(
    game_id: int,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user),
):
    return await games_service.delete_game(db, redis, game_id, current_user)
