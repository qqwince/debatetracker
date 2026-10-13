import json

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings

from app.models import Game
from app.schemas.games import GameResponse

from pydantic import TypeAdapter


async def create_game(
    db: AsyncSession,
    tournament_date,
    tournament_name,
    teammate,
    position,
    speaker_points,
    round_points,
    motion_type,
    motion_theme,
    current_user,
):

    user_id = current_user.id

    game = Game(
        tournament_date=tournament_date,
        tournament_name=tournament_name,
        teammate=teammate,
        position=position,
        speaker_points=speaker_points,
        round_points=round_points,
        motion_type=motion_type,
        motion_theme=motion_theme,
        user_id=user_id,
    )
    db.add(game)
    await db.flush()
    return game


async def get_game(
    db: AsyncSession,
    game_id,
    current_user,
    redis,
):

    if game_id:
        cache_key = f"game:{game_id}"

        cached_data = await redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

        stmt = select(Game).where(Game.user_id == current_user.id, Game.id == game_id)

    else:
        stmt = select(Game).where(Game.user_id == current_user.id)
    result = await db.execute(stmt)
    games = result.scalars().all()

    cache_ttl_seconds = settings.cache_ttl_seconds

    adapter = TypeAdapter(list[GameResponse])
    games_json = adapter.dump_json(games).decode("utf-8")

    if game_id:
        await redis.set(cache_key, games_json, ex=cache_ttl_seconds)

    return games


async def edit_game(
    db: AsyncSession,
    game_id,
    payload,
    current_user,
):
    db_game = select(Game).where(Game.id == game_id, Game.user_id == current_user.id)
    result = (await db.execute(db_game)).scalar_one_or_none()

    if not result:
        raise HTTPException(404, "Game not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(result, field, value)

    return result


async def delete_game(
    db: AsyncSession,
    game_id,
    current_user,
):
    db_game = delete(Game).where(Game.id == game_id, current_user.id == Game.user_id)
    result = await db.execute(db_game)

    if result.rowcount == 0:
        raise HTTPException(404, "Game not found")

    return result
