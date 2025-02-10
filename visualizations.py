import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import utils
import data_manager as dm

def generate_calendar_data():
    """Generate data for calendar heatmap"""
    habits_df = dm.load_habits_data()
    completion_df = dm.load_completion_data()
    
    dates = utils.get_last_n_days(30)
    data = []
    
    for date in dates:
        completed = len(completion_df[completion_df['date'] == date])
        total = len(habits_df)
        if total > 0:
            completion_rate = (completed / total) * 100
        else:
            completion_rate = 0
        data.append({
            'date': date,
            'completion_rate': completion_rate
        })
    
    return pd.DataFrame(data)

def plot_calendar_heatmap(data):
    """Create calendar heatmap visualization"""
    fig = px.line(data, x='date', y='completion_rate',
                  title='30-Day Completion Rate',
                  labels={'completion_rate': 'Completion Rate (%)',
                         'date': 'Date'})
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Completion Rate (%)",
        showlegend=False,
        height=300
    )
    
    return fig

def generate_completion_data():
    """Generate data for completion rate by habit"""
    habits_df = dm.load_habits_data()
    completion_df = dm.load_completion_data()
    
    data = []
    for _, habit in habits_df.iterrows():
        habit_name = habit['habit_name']
        total_days = (datetime.now() - datetime.strptime(habit['created_date'], '%Y-%m-%d')).days + 1
        completed_days = len(completion_df[completion_df['habit_name'] == habit_name])
        
        if total_days > 0:
            completion_rate = (completed_days / total_days) * 100
        else:
            completion_rate = 0
            
        data.append({
            'habit': habit_name,
            'completion_rate': completion_rate
        })
    
    return pd.DataFrame(data)

def plot_completion_rate(data):
    """Create completion rate visualization"""
    fig = px.bar(data, x='habit', y='completion_rate',
                 title='Habit Completion Rates',
                 labels={'completion_rate': 'Completion Rate (%)',
                        'habit': 'Habit'})
    
    fig.update_layout(
        xaxis_title="Habit",
        yaxis_title="Completion Rate (%)",
        showlegend=False,
        height=300
    )
    
    return fig
