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
        payload.round_pointer,
        payload.motion_type,
        payload.motion_theme,
        current_user
            )
    await db.commit()
    return GameResponse.model_validate(game)
