from datetime import date
from typing import List

from sqlalchemy.orm import Session

from app.models.habit_log import HabitLog
from app.services.base import BaseService


class HabitLogService(BaseService[HabitLog]):
    def get_habit_logs(
        self, db: Session, *, habit_id: int, start_date: date, end_date: date
    ) -> List[HabitLog]:
        return (
            db.query(HabitLog)
            .filter(HabitLog.habit_id == habit_id)
            .filter(HabitLog.log_date.between(start_date, end_date))
            .order_by(HabitLog.log_date)
            .all()
        )

    def log_completion(
        self, db: Session, *, habit_id: int, log_date: date, status: bool
    ) -> HabitLog:
        # Check if log already exists for this date
        existing_log = (
            db.query(HabitLog)
            .filter(HabitLog.habit_id == habit_id)
            .filter(HabitLog.log_date == log_date)
            .first()
        )

        if existing_log:
            # Use direct attribute assignment for status
            existing_log.status = status
            db.add(existing_log)
            db.commit()
            db.refresh(existing_log)
            return existing_log

        # Create new log using proper initialization
        db_obj = HabitLog()
        db_obj.habit_id = habit_id
        db_obj.log_date = log_date
        db_obj.status = status
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


habit_log_service = HabitLogService(HabitLog)
