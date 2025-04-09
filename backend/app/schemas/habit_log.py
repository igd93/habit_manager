from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HabitLogBase(BaseModel):
    habit_id: int
    value: float
    note: Optional[str] = None
    logged_at: datetime = datetime.utcnow()


class HabitLogCreate(HabitLogBase):
    pass


class HabitLogUpdate(HabitLogBase):
    value: Optional[float] = None
    note: Optional[str] = None
    logged_at: Optional[datetime] = None


class HabitLogInDBBase(HabitLogBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class HabitLog(HabitLogInDBBase):
    pass 