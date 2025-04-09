import os
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.file import File
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.user import User
from app.services.file import FileService
from app.services.habit import HabitService
from app.services.habit_log import HabitLogService
from app.services.user import UserService

# Load test environment variables
test_env_path = Path(__file__).parent / ".env.test"
if test_env_path.exists():
    with open(test_env_path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value

# Create test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    # Create the database tables
    Base.metadata.create_all(bind=engine)

    # Create a new database session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after each test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def habit_service():
    return HabitService(Habit)


@pytest.fixture(scope="function")
def user_service():
    return UserService(User)


@pytest.fixture(scope="function")
def habit_log_service():
    return HabitLogService(HabitLog)


@pytest.fixture(scope="function")
def file_service():
    return FileService(File)
