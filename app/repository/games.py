from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.models import Game
from app.repository.users import get_user
from app.schemas import GameRequest

async def create_game(
    db: AsyncSession,
    tournament_date,
    tournament_name,
    teammate,
    position,
    speaker_points,
    round_pointer,
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
        round_pointer=round_pointer,
        motion_type=motion_type,
        motion_theme=motion_theme,
        user_id=user_id,
    )
    db.add(game)
    await db.flush()
    return game

