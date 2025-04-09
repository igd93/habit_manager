from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.base import BaseService
from app.core.security import get_password_hash, verify_password


class UserService(BaseService[User]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: dict) -> User:
        db_obj = User(
            username=obj_in["username"],
            password_hash=get_password_hash(obj_in["password"]),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user


user_service = UserService(User)
