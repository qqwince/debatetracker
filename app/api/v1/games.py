from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency import get_current_user
from app.dependency import get_db
from app.models import User
from app.schemas import GameRequest, GameResponse, GameUpdate
from app.service import games as games_service

router = APIRouter()

@router.post("/game", response_model=GameResponse)
async def create_game(
    payload: GameRequest, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return await games_service.create_game(db, payload, current_user)

@router.get("/game", response_model=list[GameResponse])
async def get_game(
    db: AsyncSession = Depends(get_db),
    game_id: Optional[int] = None,
    current_user: User = Depends(get_current_user)
    ):
    return await games_service.get_game(db, game_id, current_user)

@router.patch("/game", response_model=GameResponse)
async def edit_game(
    payload: GameUpdate,
    game_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return await games_service.edit_game(db, game_id, payload, current_user)

@router.delete("/game")
async def delete_game(
    game_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await games_service.delete_game(db, game_id, current_user)