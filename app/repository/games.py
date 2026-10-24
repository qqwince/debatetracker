import json

from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import Game
from app.schemas.games import GameCursorPage, GameResponse


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


async def get_game_by_id(
    db: AsyncSession,
    redis,
    current_user,
    game_id,
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


async def get_game_pagination(
    db: AsyncSession,
    redis,
    current_user,
    limit,
    cursor,
):
    stmt = select(Game).where(Game.user_id == current_user.id)

    if (cursor is not None) and limit:
        stmt = stmt.where(Game.id < cursor)

    stmt = stmt.order_by(Game.id.desc()).limit(limit + 1)

    result = await db.execute(stmt)
    games = result.scalars().all()

    has_more = len(games) > limit
    games = games[:limit]

    next_cursor = games[-1].id if games and has_more else None

    return GameCursorPage(items=games, next_cursor=next_cursor, has_more=has_more)


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
