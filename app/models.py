from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.enum import MotionThemeEnum, MotionTypeEnum

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    game: Mapped[List["Game"]] = relationship(back_populates="user")

class Game(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True)
    entry_creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now())
    tournament_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    tournament_name: Mapped[str]
    teammate: Mapped[str]
    position: Mapped[str]
    speaker_points: Mapped[int]
    round_pointer: Mapped[int]
    motion_type: Mapped[MotionTypeEnum] #ЭПСЧ
    motion_theme: Mapped[MotionThemeEnum] #politics/economics
    
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="game")
    