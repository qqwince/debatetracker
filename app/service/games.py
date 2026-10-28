import json

from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.games import delete_game_cache, get_game_cache, set_game_cache
from app.models import User
from app.repository import games as games_repository
from app.schemas.games import GameRequest, GameResponse


async def create_game(db: AsyncSession, payload: GameRequest, current_user: User):
    game = await games_repository.create_game(
        db,
        payload.tournament_date,
        payload.tournament_name,
        payload.teammate,
        payload.position,
        payload.speaker_points,
        payload.round_points,
        payload.motion_type,
        payload.motion_theme,
        current_user,
    )
    await db.commit()
    return GameResponse.model_validate(game)


async def get_game_by_id(
    db: AsyncSession,
    redis: Redis,
    current_user: User,
    game_id: int,
):
    cached_data = await get_game_cache(redis, current_user, game_id)
    if cached_data:
        return json.loads(cached_data)
    game = await games_repository.get_game_by_id(db, current_user, game_id)
    await set_game_cache(redis, current_user, game_id, cached_info=game)
    return game


async def get_game_pagination(
    db: AsyncSession,
    redis: Redis,
    current_user: User,
    limit,
    cursor,
):
    game = await games_repository.get_game_pagination(
        db, current_user, limit, cursor
    )
    return game


async def edit_game(
    db: AsyncSession, redis: Redis, game_id: int, payload: GameRequest, current_user: User
):
    game = await games_repository.edit_game(db, game_id, payload, current_user)
    await db.commit()
    await set_game_cache(redis, current_user, game_id, cached_info=game)
    return GameResponse.model_validate(game)


async def delete_game(db: AsyncSession, redis: Redis, game_id: int, current_user: User):
    game = await games_repository.delete_game(db, game_id, current_user)
    await db.commit()
    await delete_game_cache(redis, current_user, game_id)
    return game