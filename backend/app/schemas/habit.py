from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HabitBase(BaseModel):
    title: str
    description: Optional[str] = None
    frequency: str
    target_value: float
    unit: str
    is_archived: bool = False


class HabitCreate(HabitBase):
    pass


class HabitUpdate(HabitBase):
    title: Optional[str] = None
    frequency: Optional[str] = None
    target_value: Optional[float] = None
    unit: Optional[str] = None


class HabitInDBBase(HabitBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Habit(HabitInDBBase):
    pass 