from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class HabitLogBase(BaseModel):
    habit_id: int
    value: float
    note: Optional[str] = None
    logged_at: datetime = datetime.utcnow()


class HabitLogCreate(HabitLogBase):
    log_date: date
    status: bool


class HabitLogUpdate(BaseModel):
    habit_id: Optional[int] = None
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


class HabitLogResponse(HabitLogInDBBase):
    pass
