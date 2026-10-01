from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth import decode_jwt_token
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
    
    jwt = await decode_jwt_token(credentials.credentials)
    login = jwt["sub"]
    user = await users_repository.get_user(db, login)
    
    return user