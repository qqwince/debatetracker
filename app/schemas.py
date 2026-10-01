
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.enum import MotionThemeEnum, MotionTypeEnum


class UserRequest(BaseModel):
    login: str = Field(..., max_length=127)
    password: str = Field(..., max_length=125, min_length=6)
    @field_validator('login', 'password')
    def value_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Login name cannot be empty")

        return v
    
    
class UserResponse(UserRequest):
    model_config = {"from_attributes": True}
    id: int
    
class GameRequest(BaseModel):
    entry_creation_date: datetime
    tournament_date: datetime
    tournament_name: str
    teammate: str
    position: str
    speaker_points: int
    round_points: int
    motion_type: MotionTypeEnum #ЭПСЧ
    motion_theme: MotionThemeEnum #politics/economics

class GameUpdate(BaseModel):
    entry_creation_date: Optional[datetime] = None
    tournament_date: Optional[datetime] = None
    tournament_name: Optional[str] = None
    teammate: Optional[str] = None
    position: Optional[str] = None
    speaker_points: Optional[int] = None
    round_points: Optional[int] = None
    motion_type: Optional[MotionTypeEnum] = None #ЭПСЧ
    motion_theme: Optional[MotionThemeEnum] = None #politics/economics

class GameResponse(GameRequest):
    model_config = {"from_attributes": True}
    id: int

class HashedPassword(BaseModel):
    password: str = Field(..., max_length=255)

class RefreshTokenResponse(BaseModel):
    refresh_token: str