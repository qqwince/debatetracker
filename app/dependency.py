from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.repository import users as users_repository

security = HTTPBearer()

async def get_db() -> AsyncGenerator[Session, None]:
    async with SessionLocal() as db:
        yield db
        
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), 
    db: Session = Depends(get_db),
    ) -> User:
    
    login = credentials.credentials
    user = await users_repository.get_user(db, login)
    
    if not user:
        raise HTTPException(status_code=401, detail="Unauthrozied")

    return user