from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.repository import games as games_repository
from app.repository.users import get_user
from app.schemas import GameRequest, GameResponse


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
        current_user
            )
    await db.commit()
    return GameResponse.model_validate(game)

async def get_game(db: AsyncSession, game_id: int, current_user: User):
    game = await games_repository.get_game(db, game_id, current_user)
    return game

async def edit_game(db: AsyncSession, game_id: int, payload: GameRequest, current_user: User):
    game = await games_repository.edit_game(
        db, 
        game_id,
        payload,
        current_user
    )
    await db.commit()
    return GameResponse.model_validate(game)

async def delete_game(db: AsyncSession, game_id: int, current_user: User):
    game = await games_repository.delete_game(db, game_id, current_user)
    await db.commit()
    return game