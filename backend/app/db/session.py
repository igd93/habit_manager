from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency function that creates a new SQLAlchemy SessionLocal
    that will be used in a single request, and then closes it once the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
