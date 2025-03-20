# Import all the models here to ensure they're registered with SQLAlchemy
from app.db.base_class import Base
# Import all models below
from app.models.user import User
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.file import File 