from datetime import datetime

import pytest

from app.models.habit import Habit
from app.models.user import User


def test_create_habit(db, habit_service):
    # Create a test user first
    user = User(username="test@example.com", password_hash="test123")
    db.add(user)
    db.commit()

    # Test habit creation
    habit_data = {
        "name": "Test Habit",
        "description": "Test Description",
        "user_id": user.id,
    }

    habit = habit_service.create(db, obj_in=habit_data)

    assert habit.name == "Test Habit"
    assert habit.description == "Test Description"
    assert habit.user_id == user.id
    assert habit.archived_at is None


def test_get_habit(db, habit_service):
    # Create a test user and habit
    user = User(username="test@example.com", password_hash="test123")
    db.add(user)
    db.commit()

    habit = Habit(name="Test Habit", description="Test Description", user_id=user.id)
    db.add(habit)
    db.commit()

    # Test getting the habit
    retrieved_habit = habit_service.get(db, id=habit.id)

    assert retrieved_habit is not None
    assert retrieved_habit.name == "Test Habit"
    assert retrieved_habit.id == habit.id


def test_get_user_habits(db, habit_service):
    # Create a test user
    user = User(username="test@example.com", password_hash="test123")
    db.add(user)
    db.commit()

    # Create multiple habits for the user
    habits = [Habit(name=f"Habit {i}", user_id=user.id) for i in range(3)]
    for habit in habits:
        db.add(habit)
    db.commit()

    # Test getting user habits
    user_habits = habit_service.get_user_habits(db, user_id=user.id)

    assert len(user_habits) == 3
    assert all(habit.user_id == user.id for habit in user_habits)
    assert all(habit.archived_at is None for habit in user_habits)


def test_archive_habit(db, habit_service):
    # Create a test user and habit
    user = User(username="test@example.com", password_hash="test123")
    db.add(user)
    db.commit()

    habit = Habit(name="Test Habit", description="Test Description", user_id=user.id)
    db.add(habit)
    db.commit()

    # Test archiving the habit
    archived_habit = habit_service.archive(db, habit_id=habit.id, user_id=user.id)

    assert archived_habit is not None
    assert archived_habit.archived_at is not None
    assert archived_habit.id == habit.id


def test_archive_nonexistent_habit(db, habit_service):
    # Test archiving a non-existent habit
    archived_habit = habit_service.archive(db, habit_id=999, user_id=1)
    assert archived_habit is None


def test_update_habit(db, habit_service):
    # Create a test user and habit
    user = User(username="test@example.com", password_hash="test123")
    db.add(user)
    db.commit()

    habit = Habit(name="Test Habit", description="Test Description", user_id=user.id)
    db.add(habit)
    db.commit()

    # Test updating the habit
    update_data = {"name": "Updated Habit", "description": "Updated Description"}

    updated_habit = habit_service.update(db, db_obj=habit, obj_in=update_data)

    assert updated_habit.name == "Updated Habit"
    assert updated_habit.description == "Updated Description"


def test_delete_habit(db, habit_service):
    # Create a test user and habit
    user = User(username="test@example.com", password_hash="test123")
    db.add(user)
    db.commit()

    habit = Habit(name="Test Habit", description="Test Description", user_id=user.id)
    db.add(habit)
    db.commit()

    # Test deleting the habit
    deleted_habit = habit_service.delete(db, id=habit.id)

    assert deleted_habit.id == habit.id
    # Verify the habit is deleted
    assert habit_service.get(db, id=habit.id) is None
