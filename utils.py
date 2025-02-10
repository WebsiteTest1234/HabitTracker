from datetime import datetime, timedelta
import pandas as pd

def get_date_string(date=None):
    """Return date string in YYYY-MM-DD format"""
    if date is None:
        date = datetime.now()
    return date.strftime('%Y-%m-%d')

def calculate_streak(completion_dates):
    """Calculate current streak for a habit"""
    if not completion_dates:
        return 0
        
    dates = sorted([datetime.strptime(date, '%Y-%m-%d') for date in completion_dates])
    today = datetime.now().date()
    current_streak = 0
    
    for i in range(len(dates)-1, -1, -1):
        date = dates[i].date()
        if (today - date).days > current_streak:
            break
        current_streak += 1
    
    return current_streak

def get_last_n_days(n):
    """Get list of last n days including today"""
    today = datetime.now()
    return [(today - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(n-1, -1, -1)]
