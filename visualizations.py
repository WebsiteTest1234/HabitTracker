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
    """Create calendar heatmap visualization with grid layout"""
    # Convert dates to datetime objects
    data['date'] = pd.to_datetime(data['date'])

    # Create calendar heatmap
    fig = go.Figure()

    # Add heatmap trace
    fig.add_trace(go.Heatmap(
        x=[d.day for d in data['date']],
        y=[d.strftime('%B') for d in data['date']],
        z=data['completion_rate'],
        colorscale='RdYlGn',
        showscale=True,
        name='Completion Rate'
    ))

    # Update layout with grid styling
    fig.update_layout(
        title='Monthly Habit Completion Rate',
        xaxis_title='Day of Month',
        yaxis_title='Month',
        height=400,
        xaxis=dict(
            tickmode='array',
            ticktext=list(range(1, 32)),
            tickvals=list(range(1, 32)),
            gridcolor='rgba(128, 128, 128, 0.2)',
            showgrid=True,
            dtick=1
        ),
        yaxis=dict(
            gridcolor='rgba(128, 128, 128, 0.2)',
            showgrid=True
        ),
        plot_bgcolor='white'
    )

    # Add grid lines
    for i in range(32):
        fig.add_shape(
            type="line",
            x0=i-0.5, x1=i-0.5,
            y0=-0.5, y1=0.5,
            line=dict(color="rgba(128, 128, 128, 0.2)", width=1)
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