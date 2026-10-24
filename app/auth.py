import secrets
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from redis import Redis

from app.config import settings

# Настраиваем контекст хеширования (по умолчанию bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Security
security = HTTPBearer()

_jwt_secret_key: str | None = None


async def get_jwt_secret_key() -> str:
    """Get JWT secret key from settings or generate a consistent one."""
    global _jwt_secret_key

    # First, try to get from settings
    if hasattr(settings, "JWT_SECRET_KEY") and settings.JWT_SECRET_KEY:
        return settings.JWT_SECRET_KEY

    # If not in settings, generate once and store globally
    if _jwt_secret_key is None:
        _jwt_secret_key = secrets.token_urlsafe(32)
        print(f"Generated JWT secret key: {_jwt_secret_key}")  # For debugging

    return _jwt_secret_key


async def create_jwt_token(
    username: str, expires_delta: timedelta | None = None
) -> str:
    """Create a JWT token for the user."""
    cache_ttl_seconds = settings.cache_ttl_seconds
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(seconds=cache_ttl_seconds)

    payload = {
        "sub": username,  # Subject (user identifier)
        "exp": int(expire.timestamp()),  # Expiration time as Unix timestamp
        "iat": int(datetime.now(UTC).timestamp()),  # Issued at as Unix timestamp
        "jti": secrets.token_urlsafe(16),  # JWT ID (unique identifier)
    }

    return jwt.encode(payload, await get_jwt_secret_key(), algorithm="HS256")


async def create_refresh_token(
    username: str,
    redis: Redis,
) -> str:
    """Create a refresh token for the user."""
    expire = settings.cache_ttl_refresh_seconds

    refresh_token = secrets.token_urlsafe(32)

    await redis.set(f"refresh:{refresh_token}", username, expire)

    return refresh_token


async def create_token_pair(username: str, redis: Redis) -> tuple[str, str]:
    """Create both access and refresh tokens for the user."""
    access_token = await create_jwt_token(username)
    refresh_token = await create_refresh_token(username, redis)
    return access_token, refresh_token


async def validate_refresh_token(refresh_token: str, redis: Redis) -> str:
    """Validate refresh token and return username."""
    token = await redis.get(f"refresh:{refresh_token}")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    jwt = await create_jwt_token(token)

    return jwt


async def decode_jwt_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    try:
        # Decode the token
        payload = jwt.decode(token, await get_jwt_secret_key(), algorithms=["HS256"])
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


async def get_current_user_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Extract and validate the current user from JWT token."""
    token = credentials.credentials
    payload = decode_jwt_token(token)
    username = payload.get("sub")

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    return username


###


async def hash_password(password: str) -> str:
    """Генерирует хеш пароля с автоматической солью."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Сравнивает чистый пароль с хешем из БД."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )
