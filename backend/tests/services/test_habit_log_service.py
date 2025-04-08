import pytest
from datetime import date, datetime, timedelta
from app.models.habit_log import HabitLog
from app.models.habit import Habit
from app.models.user import User

def test_create_habit_log(db, habit_log_service):
    # Create test user and habit
    user = User(username="test@example.com", password_hash="test123")
    db.add(user)
    db.commit()
    
    habit = Habit(
        name="Test Habit",        
        user_id=user.id
    )
    db.add(habit)
    db.commit()
    
    # Test creating a habit log
    log_date = date.today()
    log = habit_log_service.log_completion(
        db, habit_id=habit.id, log_date=log_date, status=True
    )
    
    assert log.habit_id == habit.id
    assert log.log_date == log_date
    assert log.status is True
    assert log.created_at is not None

def test_get_habit_logs(db, habit_log_service):
    # Create test user and habit
    user = User(username="test@example.com", password_hash="test123")
    db.add(user)
    db.commit()
    
    habit = Habit(
        name="Test Habit",        
        user_id=user.id
    )
    db.add(habit)
    db.commit()
    
    # Create multiple logs for different dates
    today = date.today()
    yesterday = date.fromordinal(today.toordinal() - 1)
    
    log1 = HabitLog(
        habit_id=habit.id,
        log_date=today,
        status=True
    )
    log2 = HabitLog(
        habit_id=habit.id,
        log_date=yesterday,
        status=False
    )
    db.add(log1)
    db.add(log2)
    db.commit()
    
    # Test getting logs within date range
    logs = habit_log_service.get_habit_logs(
        db, habit_id=habit.id, start_date=yesterday, end_date=today
    )
    
    assert len(logs) == 2
    assert all(log.habit_id == habit.id for log in logs)
    assert {log.log_date for log in logs} == {today, yesterday}

def test_update_existing_log(db, habit_log_service):
    # Create test user and habit
    user = User(username="test@example.com", password_hash="test123")
    db.add(user)
    db.commit()
    
    habit = Habit(
        name="Test Habit",        
        user_id=user.id
    )
    db.add(habit)
    db.commit()
    
    # Create initial log with fixed timestamp
    log_date = date.today()
    initial_time = datetime(2025, 1, 1, 12, 0, 0)  # Fixed initial time
    initial_log = HabitLog(
        habit_id=habit.id,
        log_date=log_date,
        status=True,
        created_at=initial_time,
        updated_at=initial_time  # Set both timestamps to initial time
    )
    db.add(initial_log)
    db.commit()
    
    # Force a later timestamp for the update
    update_time = datetime(2025, 1, 1, 12, 0, 1)  # One second later
    initial_log.updated_at = update_time
    db.add(initial_log)
    db.commit()
    
    # Test updating existing log
    updated_log = habit_log_service.log_completion(
        db, habit_id=habit.id, log_date=log_date, status=False
    )
    
    assert updated_log.status is False
    assert updated_log.updated_at > initial_log.created_at

def test_get_habit_logs_empty_range(db, habit_log_service):
    # Create test user and habit
    user = User(username="test@example.com", password_hash="test123")
    db.add(user)
    db.commit()
    
    habit = Habit(
        name="Test Habit",        
        user_id=user.id
    )
    db.add(habit)
    db.commit()
    
    # Test getting logs with no entries in range
    today = date.today()
    tomorrow = date.fromordinal(today.toordinal() + 1)
    
    logs = habit_log_service.get_habit_logs(
        db, habit_id=habit.id, start_date=today, end_date=tomorrow
    )
    
    assert len(logs) == 0

def test_get_habit_logs_nonexistent_habit(db, habit_log_service):
    # Test getting logs for non-existent habit
    today = date.today()
    logs = habit_log_service.get_habit_logs(
        db, habit_id=999, start_date=today, end_date=today
    )
    
    assert len(logs) == 0 