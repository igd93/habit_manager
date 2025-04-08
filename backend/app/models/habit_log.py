from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class HabitLog(Base):
    __tablename__ = "habit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    log_date = Column(Date, nullable=False)
    status = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Define relationships
    habit = relationship("Habit", back_populates="logs") 