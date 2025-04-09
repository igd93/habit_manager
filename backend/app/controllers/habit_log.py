from datetime import date
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.habit_log import HabitLogCreate, HabitLogResponse
from app.services.habit import habit_service
from app.services.habit_log import habit_log_service

router = APIRouter()


@router.post("/{habit_id}/log", response_model=HabitLogResponse)
def log_habit_completion(
    *,
    db: Session = Depends(get_db),
    habit_id: int,
    log_in: HabitLogCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Log habit completion for a specific date.
    """
    # Verify habit belongs to user
    habit = habit_service.get(db, id=habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    if habit.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    log = habit_log_service.log_completion(
        db, habit_id=habit_id, log_date=log_in.log_date, status=log_in.status
    )
    return log


@router.get("/{habit_id}/log", response_model=List[HabitLogResponse])
def get_habit_logs(
    *,
    db: Session = Depends(get_db),
    habit_id: int,
    start_date: date = Query(...),
    end_date: date = Query(...),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get habit logs for a date range.
    """
    # Verify habit belongs to user
    habit = habit_service.get(db, id=habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    if habit.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    logs = habit_log_service.get_habit_logs(
        db, habit_id=habit_id, start_date=start_date, end_date=end_date
    )
    return logs
