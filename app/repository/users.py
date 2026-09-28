from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import create_jwt_token, hash_password
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

