from fastapi import APIRouter, Cookie, Depends, Response
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import validate_refresh_token
from app.cache.cache import get_redis
from app.dependency import get_current_user, get_db
from app.models import User
from app.schemas.users import (
    AuthResponse,
    UserRequest,
    UserResponse,
)
from app.service import users as users_service

router = APIRouter()


@router.post("/users/register", response_model=AuthResponse)
async def create_user(
    payload: UserRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    tokens = await users_service.create_user(db, redis, payload.login, payload.password)
    response.set_cookie(key="refresh_token", value=tokens['refresh_token'], samesite="strict", httponly=True)
    return {
            "access_token":tokens['access_token']
    }


@router.post("/users/login", response_model=AuthResponse)
async def login_user(
    payload: UserRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    tokens = await users_service.login_user(db, redis, payload.login, payload.password)
    response.set_cookie(key="refresh_token", value=tokens['refresh_token'], samesite="strict", httponly=True)
    return {
            "access_token":tokens['access_token']
        }

@router.delete("/users/logout")
async def logout_user(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    redis: Redis = Depends(get_redis),
):
    logout = await users_service.logout_user(refresh_token, redis)
    response.delete_cookie(key='refresh_token')
    return logout


@router.get("/users/me", response_model=UserResponse)
async def get_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/users/refresh", response_model=str)
async def refresh_token(
    refresh_token: str | None = Cookie(default=None),
    redis: Redis = Depends(get_redis),
    ):
    return await validate_refresh_token(refresh_token, redis)