import pytest

from app.models.file import File
from app.models.user import User


def test_create_file(db, file_service):
    # Create test user
    user = User(username="testuser", password_hash="test123")
    db.add(user)
    db.commit()

    # Test file creation
    filename = "test_file.txt"
    storage_key = "test/storage/key"

    file = file_service.create_file(
        db, uploader_id=user.id, filename=filename, storage_key=storage_key
    )

    assert file.filename == filename
    assert file.storage_key == storage_key
    assert file.uploader_id == user.id
    assert file.id is not None


def test_get_user_files(db, file_service):
    # Create test user
    user = User(username="testuser", password_hash="test123")
    db.add(user)
    db.commit()

    # Create multiple files for the user
    files = [
        File(
            uploader_id=user.id,
            filename=f"file_{i}.txt",
            storage_key=f"test/storage/key_{i}",
        )
        for i in range(3)
    ]
    for file in files:
        db.add(file)
    db.commit()

    # Test getting user files
    user_files = file_service.get_user_files(db, user_id=user.id)

    assert len(user_files) == 3
    assert all(file.uploader_id == user.id for file in user_files)
    assert {file.filename for file in user_files} == {f"file_{i}.txt" for i in range(3)}


def test_get_user_files_with_pagination(db, file_service):
    # Create test user
    user = User(username="testuser", password_hash="test123")
    db.add(user)
    db.commit()

    # Create multiple files for the user
    files = [
        File(
            uploader_id=user.id,
            filename=f"file_{i}.txt",
            storage_key=f"test/storage/key_{i}",
        )
        for i in range(5)
    ]
    for file in files:
        db.add(file)
    db.commit()

    # Test pagination
    first_page = file_service.get_user_files(db, user_id=user.id, skip=0, limit=2)
    second_page = file_service.get_user_files(db, user_id=user.id, skip=2, limit=2)

    assert len(first_page) == 2
    assert len(second_page) == 2
    assert {file.id for file in first_page} != {file.id for file in second_page}


def test_get_user_files_empty(db, file_service):
    # Create test user
    user = User(username="testuser", password_hash="test123")
    db.add(user)
    db.commit()

    # Test getting files for user with no files
    user_files = file_service.get_user_files(db, user_id=user.id)
    assert len(user_files) == 0


def test_get_user_files_nonexistent_user(db, file_service):
    # Test getting files for non-existent user
    user_files = file_service.get_user_files(db, user_id=999)
    assert len(user_files) == 0
