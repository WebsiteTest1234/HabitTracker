import pandas as pd
from datetime import datetime
import json
import os
import utils
from models import db, User, Habit, Completion
from flask_login import current_user

def load_habits_data():
    """Load habits data for current user"""
    if not current_user.is_authenticated:
        return pd.DataFrame(columns=['habit_name', 'category', 'created_date'])

    habits = Habit.query.filter_by(user_id=current_user.id).all()
    data = [{
        'habit_name': habit.habit_name,
        'category': habit.category,
        'created_date': habit.created_date
    } for habit in habits]

    return pd.DataFrame(data)

def load_completion_data():
    """Load completion data for current user"""
    if not current_user.is_authenticated:
        return pd.DataFrame(columns=['habit_name', 'date', 'completed'])

    completions = Completion.query.join(Habit).filter(Habit.user_id == current_user.id).all()
    data = [{
        'habit_name': h.habit_name,
        'date': c.date,
        'completed': c.completed
    } for c in completions for h in [Habit.query.get(c.habit_id)]] #Join to get habit name

    return pd.DataFrame(data)

def add_habit(habit_name, category):
    """Add a new habit for current user"""
    if not current_user.is_authenticated:
        return

    habit = Habit(
        user_id=current_user.id,
        habit_name=habit_name,
        category=category,
        created_date=utils.get_date_string()
    )
    db.session.add(habit)
    db.session.commit()

def mark_habit_complete(habit_name):
    """Mark a habit as complete for today"""
    if not current_user.is_authenticated:
        return

    habit = Habit.query.filter_by(
        user_id=current_user.id,
        habit_name=habit_name
    ).first()

    if habit:
        today = utils.get_date_string()
        completion = Completion.query.filter_by(
            habit_id=habit.id,
            date=today
        ).first()

        if not completion:
            completion = Completion(habit_id=habit.id, date=today)
            db.session.add(completion)
            db.session.commit()

def mark_habit_incomplete(habit_name):
    """Mark a habit as incomplete for today"""
    if not current_user.is_authenticated:
        return

    habit = Habit.query.filter_by(
        user_id=current_user.id,
        habit_name=habit_name
    ).first()

    if habit:
        today = utils.get_date_string()
        completion = Completion.query.filter_by(
            habit_id=habit.id,
            date=today
        ).first()

        if completion:
            db.session.delete(completion)
            db.session.commit()

def is_habit_completed_today(habit_name):
    """Check if a habit is completed today"""
    if not current_user.is_authenticated:
        return False

    habit = Habit.query.filter_by(
        user_id=current_user.id,
        habit_name=habit_name
    ).first()

    if habit:
        today = utils.get_date_string()
        completion = Completion.query.filter_by(
            habit_id=habit.id,
            date=today
        ).first()
        return completion is not None
    return False

def get_completed_habits_count_today():
    """Get count of completed habits for today"""
    if not current_user.is_authenticated:
        return 0

    today = utils.get_date_string()
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    count = 0

    for habit in habits:
        if Completion.query.filter_by(
            habit_id=habit.id,
            date=today
        ).first():
            count += 1

    return count

def get_habit_completion_dates(habit_name):
    """Get all completion dates for a habit"""
    if not current_user.is_authenticated:
        return []

    habit = Habit.query.filter_by(
        user_id=current_user.id,
        habit_name=habit_name
    ).first()

    if habit:
        completions = Completion.query.filter_by(habit_id=habit.id).all()
        return [completion.date for completion in completions]
    return []