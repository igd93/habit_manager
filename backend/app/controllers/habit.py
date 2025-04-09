from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.habit import Habit, HabitCreate, HabitUpdate
from app.services.habit import habit_service

router = APIRouter()


@router.post("/", response_model=Habit, status_code=status.HTTP_201_CREATED)
def create_habit(
    *,
    db: Session = Depends(get_db),
    habit_in: HabitCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new habit.
    """
    habit = habit_service.create(
        db, obj_in={"**": habit_in.dict(), "user_id": int(current_user.id)}
    )
    return habit


@router.get("/", response_model=List[Habit])
def read_habits(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve habits.
    """
    habits = habit_service.get_user_habits(
        db, user_id=int(current_user.id), skip=skip, limit=limit
    )
    return habits


@router.get("/{habit_id}", response_model=Habit)
def read_habit(
    *,
    db: Session = Depends(get_db),
    habit_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get habit by ID.
    """
    habit = habit_service.get(db, id=habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    if habit.user_id != int(current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return habit


@router.put("/{habit_id}", response_model=Habit)
def update_habit(
    *,
    db: Session = Depends(get_db),
    habit_id: int,
    habit_in: HabitUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update a habit.
    """
    habit = habit_service.get(db, id=habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    if habit.user_id != int(current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    habit = habit_service.update(db, db_obj=habit, obj_in=habit_in)
    return habit


@router.delete("/{habit_id}", response_model=Habit)
def delete_habit(
    *,
    db: Session = Depends(get_db),
    habit_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Archive a habit.
    """
    habit = habit_service.archive(db, habit_id=habit_id, user_id=int(current_user.id))
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit
