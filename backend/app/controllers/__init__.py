from app.controllers.auth import router as auth_router
from app.controllers.user import router as user_router
from app.controllers.habit import router as habit_router
from app.controllers.habit_log import router as habit_log_router

__all__ = ["auth_router", "user_router", "habit_router", "habit_log_router"]
