from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import os
from dotenv import load_dotenv

from app.config import settings

load_dotenv()

DB_HOST = settings.DB_HOST
DB_PORT = settings.DB_PORT
DB_USER_NAME = settings.DB_USER_NAME
DB_NAME = settings.DB_NAME
DB_PASSWORD = settings.DB_PASSWORD

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER_NAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()
