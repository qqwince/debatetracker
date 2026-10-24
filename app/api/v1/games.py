from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.cache import get_redis
from app.dependency import get_current_user, get_db
from app.models import User
from app.schemas.games import GameRequest, GameResponse, GameUpdate
from app.service import games as games_service

router = APIRouter()


@router.post("/game", response_model=GameResponse)
async def create_game(
    payload: GameRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await games_service.create_game(db, payload, current_user)


@router.get("/game/{game_id}", response_model=list[GameResponse])
async def get_game_by_id(
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user),
    game_id: int | None = None,
):
    return await games_service.get_game_by_id(db, redis, current_user, game_id)


@router.get("/game")
async def get_game_pagination(
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user),
    limit: int = None,
    cursor: int | None = None,
):
    return await games_service.get_game_pagination(
        db, redis, current_user, limit, cursor
    )


@router.patch("/game", response_model=GameResponse)
async def edit_game(
    payload: GameUpdate,
    game_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await games_service.edit_game(db, game_id, payload, current_user)


@router.delete("/game")
async def delete_game(
    game_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await games_service.delete_game(db, game_id, current_user)
