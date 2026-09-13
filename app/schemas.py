
from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.enum import MotionThemeEnum, MotionTypeEnum


class UserRequest(BaseModel):
    login: str = Field(..., max_length=127)
    @field_validator('login')
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
    round_pointer: int
    motion_type: MotionTypeEnum #ЭПСЧ
    motion_theme: MotionThemeEnum #politics/economics

class GameResponse(GameRequest):
    model_config = {"from_attributes": True}
    id: int