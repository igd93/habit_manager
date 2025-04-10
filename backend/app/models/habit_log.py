from datetime import date, datetime

from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class HabitLog(Base):
    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return "habit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id"), nullable=False)
    log_date: Mapped[date] = mapped_column(nullable=False)
    status: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Define relationships
    habit = relationship("Habit", back_populates="logs")
