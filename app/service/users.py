from fastapi import HTTPException
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository import users as users_repository

async def create_user(db: AsyncSession, redis: Redis, login: str, password: str):
    if await users_repository.get_user(db, login):
        raise HTTPException(status_code=400, detail="User already exists")
    response = await users_repository.create_user(db, redis, login, password)
    await db.commit()
    return response


async def login_user(db: AsyncSession, redis: Redis, login: str, password: str):
    response = await users_repository.login_user(db, redis, login, password)
    await db.commit()
    return response
