import pytest
from app.models.user import User


def test_create_user(db, user_service):
    # Test user creation
    user_data = {"username": "testuser", "password": "testpassword123"}

    user = user_service.create(db, obj_in=user_data)

    assert user.username == "testuser"
    assert user.password_hash != "testpassword123"  # Password should be hashed
    assert user.id is not None


def test_get_by_username(db, user_service):
    # Create a test user
    user_data = {"username": "testuser", "password": "testpassword123"}
    user = user_service.create(db, obj_in=user_data)

    # Test getting user by username
    retrieved_user = user_service.get_by_username(db, username="testuser")

    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.id == user.id


def test_get_by_username_not_found(db, user_service):
    # Test getting non-existent user
    retrieved_user = user_service.get_by_username(db, username="nonexistent")
    assert retrieved_user is None


def test_authenticate_user(db, user_service):
    # Create a test user
    user_data = {"username": "testuser", "password": "testpassword123"}
    user = user_service.create(db, obj_in=user_data)

    # Test successful authentication
    authenticated_user = user_service.authenticate(
        db, username="testuser", password="testpassword123"
    )

    assert authenticated_user is not None
    assert authenticated_user.username == "testuser"
    assert authenticated_user.id == user.id


def test_authenticate_wrong_password(db, user_service):
    # Create a test user
    user_data = {"username": "testuser", "password": "testpassword123"}
    user_service.create(db, obj_in=user_data)

    # Test authentication with wrong password
    authenticated_user = user_service.authenticate(
        db, username="testuser", password="wrongpassword"
    )

    assert authenticated_user is None


def test_authenticate_nonexistent_user(db, user_service):
    # Test authentication with non-existent user
    authenticated_user = user_service.authenticate(
        db, username="nonexistent", password="testpassword123"
    )

    assert authenticated_user is None


def test_get_user(db, user_service):
    # Create a test user
    user_data = {"username": "testuser", "password": "testpassword123"}
    user = user_service.create(db, obj_in=user_data)

    # Test getting user by ID
    retrieved_user = user_service.get(db, id=user.id)

    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.id == user.id


def test_get_nonexistent_user(db, user_service):
    # Test getting non-existent user by ID
    retrieved_user = user_service.get(db, id=999)
    assert retrieved_user is None
