# Import all the models here to ensure they're registered with SQLAlchemy
from app.db.base_class import Base
from app.models.file import File
from app.models.habit import Habit
from app.models.habit_log import HabitLog

# Import all models below
from app.models.user import User
