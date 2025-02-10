import pandas as pd
from datetime import datetime
import json
import os
import utils

HABITS_FILE = "habits.csv"
COMPLETION_FILE = "completions.csv"

def load_habits_data():
    """Load habits data from CSV file"""
    if os.path.exists(HABITS_FILE):
        return pd.read_csv(HABITS_FILE)
    return pd.DataFrame(columns=['habit_name', 'category', 'created_date'])

def load_completion_data():
    """Load completion data from CSV file"""
    if os.path.exists(COMPLETION_FILE):
        return pd.read_csv(COMPLETION_FILE)
    return pd.DataFrame(columns=['habit_name', 'date', 'completed'])

def save_habits_data(df):
    """Save habits data to CSV file"""
    df.to_csv(HABITS_FILE, index=False)

def save_completion_data(df):
    """Save completion data to CSV file"""
    df.to_csv(COMPLETION_FILE, index=False)

def add_habit(habit_name, category):
    """Add a new habit"""
    habits_df = load_habits_data()
    if habit_name not in habits_df['habit_name'].values:
        new_habit = pd.DataFrame({
            'habit_name': [habit_name],
            'category': [category],
            'created_date': [utils.get_date_string()]
        })
        habits_df = pd.concat([habits_df, new_habit], ignore_index=True)
        save_habits_data(habits_df)

def mark_habit_complete(habit_name):
    """Mark a habit as complete for today"""
    completion_df = load_completion_data()
    today = utils.get_date_string()
    
    # Remove any existing entry for today
    completion_df = completion_df[
        ~((completion_df['habit_name'] == habit_name) & 
          (completion_df['date'] == today))
    ]
    
    # Add new completion entry
    new_completion = pd.DataFrame({
        'habit_name': [habit_name],
        'date': [today],
        'completed': [True]
    })
    completion_df = pd.concat([completion_df, new_completion], ignore_index=True)
    save_completion_data(completion_df)

def mark_habit_incomplete(habit_name):
    """Mark a habit as incomplete for today"""
    completion_df = load_completion_data()
    today = utils.get_date_string()
    
    completion_df = completion_df[
        ~((completion_df['habit_name'] == habit_name) & 
          (completion_df['date'] == today))
    ]
    save_completion_data(completion_df)

def is_habit_completed_today(habit_name):
    """Check if a habit is completed today"""
    completion_df = load_completion_data()
    today = utils.get_date_string()
    return any(
        (completion_df['habit_name'] == habit_name) & 
        (completion_df['date'] == today)
    )

def get_completed_habits_count_today():
    """Get count of completed habits for today"""
    completion_df = load_completion_data()
    today = utils.get_date_string()
    return len(completion_df[completion_df['date'] == today])

def get_habit_completion_dates(habit_name):
    """Get all completion dates for a habit"""
    completion_df = load_completion_data()
    return completion_df[completion_df['habit_name'] == habit_name]['date'].tolist()
