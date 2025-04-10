from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.file import File
from app.models.habit import Habit


class User(Base):
    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Define relationships
    habit: Mapped[List["Habit"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    files: Mapped[List["File"]] = relationship(
        back_populates="uploader", cascade="all, delete-orphan"
    )
