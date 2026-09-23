from fastapi import HTTPException
from sqlalchemy import delete, select
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
    ):
    if game_id:
        stmt = select(Game).where(Game.user_id == current_user.id, Game.id == game_id)
    else:
        stmt = select(Game).where(Game.user_id == current_user.id)
    result = await db.execute(stmt)
    games = result.scalars().all()
    
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
        raise HTTPException(
            404,
            "Game not found"
        )
    
    
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
        raise HTTPException(
            404,
            "Game not found"
        )
    
    
    return result