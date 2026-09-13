from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency import get_current_user, get_db
from app.models import User
from app.schemas import GameRequest, GameResponse
from app.service import games as games_service

router = APIRouter()

@router.post("/game", response_model=GameResponse)
async def create_game(
    payload: GameRequest, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    return await games_service.create_game(db, payload, current_user)