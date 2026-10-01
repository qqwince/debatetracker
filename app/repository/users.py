from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import create_jwt_token, hash_password, verify_password
from app.models import User
from app.schemas import HashedPassword, UserResponse

async def get_user(db: AsyncSession, login: str) -> User | None:
    result = await db.execute(
        select(User).where(User.login == login)
        )
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, login: str, password: str) -> UserResponse:
    hashed_password: HashedPassword = hash_password(password)
    access_token = create_jwt_token(login)
    
    user = User(login=login, password=hashed_password)
    db.add(user)
    
    await db.flush()
    return {
        "access_token": access_token
    }

async def login_user(db: AsyncSession, login: str, password: str) -> UserResponse:
    
    user = await get_user(db=db, login=login)
    #hashed_password: HashedPassword = hash_password(password)
    if not user:
        raise HTTPException(
                    401,
                    "Incorrect login or password"
        )
        
    is_verified = verify_password(password, user.password)
    
    if is_verified == False:
        raise HTTPException(
            401,
            "Incorrect login or password"
        )
    access_token = create_jwt_token(login)
    return {
        "access_token": access_token
    }