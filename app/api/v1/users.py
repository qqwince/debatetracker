from fastapi import APIRouter, Depends
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import validate_refresh_token
from app.cache.cache import get_redis
from app.dependency import get_current_user
from app.dependency import get_db
from app.models import User
from app.schemas import UserRequest, UserResponse
from app.service import users as users_service

router = APIRouter()

@router.post("/users/register")
async def create_user(payload: UserRequest, db: AsyncSession = Depends(get_db), redis: Redis = Depends(get_redis)):
    return await users_service.create_user(db, redis, payload.login, payload.password)

@router.post("/users/login")
async def login_user(payload: UserRequest, db: AsyncSession = Depends(get_db), redis: Redis = Depends(get_redis)):
    return await users_service.login_user(db, redis, payload.login, payload.password)

@router.get(
    "/users/me",
    responses={
        200: {"description": "Successful response"},
        401: {
            "description": "Unauthorized: Invalid or missing token"
        }
    }
)
async def get_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/users/refresh")
async def refresh_token(refresh_token: str, redis: Redis = Depends(get_redis)):
    return await validate_refresh_token(refresh_token, redis)

    """
    payload: RefreshTokenResponse, 
    redis: Redis = Depends(get_redis)
    """