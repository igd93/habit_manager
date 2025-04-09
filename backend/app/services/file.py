from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.file import File
from app.services.base import BaseService


class FileService(BaseService[File]):
    def get_user_files(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[File]:
        return (
            db.query(File)
            .filter(File.uploader_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_file(
        self, db: Session, *, uploader_id: int, filename: str, storage_key: str
    ) -> File:
        db_obj = File(
            uploader_id=uploader_id, filename=filename, storage_key=storage_key
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


file_service = FileService(File)
