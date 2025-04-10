from datetime import UTC, datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.habit import Habit
from app.services.base import BaseService


class HabitService(BaseService[Habit]):
    def get_user_habits(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Habit]:
        return (
            db.query(Habit)
            .filter(Habit.user_id == user_id)
            .filter(Habit.archived_at.is_(None))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def archive(self, db: Session, *, habit_id: int, user_id: int) -> Optional[Habit]:
        habit = self.get(db, id=habit_id)
        if not habit or habit.user_id != user_id:
            return None
        habit.archived_at = datetime.now(UTC)
        db.add(habit)
        db.commit()
        db.refresh(habit)
        return habit


habit_service = HabitService(Habit)
