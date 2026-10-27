from fastapi import HTTPException
from redis import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import create_token_pair, hash_password, verify_password
from app.models import User
from app.schemas.users import HashedPassword, RefreshToken, UserResponse


async def get_user(db: AsyncSession, login: str) -> User | None:
    result = await db.execute(select(User).where(User.login == login))
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession, redis: Redis, login: str, password: str
) -> UserResponse:
    hashed_password: HashedPassword = await hash_password(password)
    access_token, refresh_token = await create_token_pair(login, redis)

    user = User(login=login, password=hashed_password)
    db.add(user)

    await db.flush()
    return {"access_token": access_token, "refresh_token": refresh_token}


async def login_user(
    db: AsyncSession, redis: Redis, login: str, password: str
) -> UserResponse:

    user = await get_user(db=db, login=login)
    if not user:
        raise HTTPException(401, "Incorrect login or password")

    is_verified = await verify_password(password, user.password)

    if not is_verified:
        raise HTTPException(401, "Incorrect login or password")
    access_token, refresh_token = await create_token_pair(login, redis)
    return {"access_token": access_token, "refresh_token": refresh_token}

async def logout_user(
    refresh_token: RefreshToken,
    redis: Redis, 
    ):
    await redis.delete(f"refresh:{refresh_token}")
    return "successfully"