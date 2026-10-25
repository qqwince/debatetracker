from datetime import datetime

from pydantic import BaseModel, Field

from app.enum import MotionThemeEnum, MotionTypeEnum


class GameRequest(BaseModel):
    entry_creation_date: datetime
    tournament_date: datetime
    tournament_name: str
    teammate: str
    position: str
    speaker_points: int
    round_points: int
    motion_type: MotionTypeEnum  # ЭПСЧ
    motion_theme: MotionThemeEnum  # politics/economics


class GameUpdate(BaseModel):
    entry_creation_date: datetime | None = None
    tournament_date: datetime | None = None
    tournament_name: str | None = None
    teammate: str | None = None
    position: str | None = None
    speaker_points: int | None = None
    round_points: int | None = None
    motion_type: MotionTypeEnum | None = None  # ЭПСЧ
    motion_theme: MotionThemeEnum | None = None  # politics/economics


class GameResponse(GameRequest):
    model_config = {"from_attributes": True}
    id: int

class GamePaginationResponse(BaseModel):
    model_config = {"from_attributes": True}
    items: list[GameResponse]
    next_cursor: int | None
    has_more: bool


class GameCursorPage(BaseModel):
    items: list[GameResponse]
    next_cursor: int | None
    has_more: bool


class GameListParams(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    cursor: int | None = Field(default=None, gt=0)
