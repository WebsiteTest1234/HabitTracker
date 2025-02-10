import streamlit as st
import pandas as pd
from datetime import datetime
import utils
import data_manager as dm
import visualizations as viz
from styles import apply_styles
from flask import Flask
from flask_login import LoginManager, current_user, login_required
from models import db, User
from auth import login_page, signup_page
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_db():
    with app.app_context():
        db.create_all()

def main():
    st.set_page_config(page_title="Habit Tracker", layout="wide")
    apply_styles()

    # Initialize database
    init_db()

    # Session state for authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # Check if user is authenticated
    if not st.session_state.authenticated:
        # Handle login/signup routing
        path = st.experimental_get_query_params().get("page", ["login"])[0]

        if path == "signup":
            signup_page()
        else:
            login_page()
        return

    st.title("🎯 Habit Tracker")

    # Add logout button in sidebar
    with st.sidebar:
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.experimental_rerun()

    # Initialize session state
    if 'habits_data' not in st.session_state:
        st.session_state.habits_data = dm.load_habits_data()

    # Sidebar for adding new habits
    with st.sidebar:
        st.header("Add New Habit")
        new_habit = st.text_input("Habit Name")
        habit_category = st.selectbox("Category", ["Health", "Productivity", "Learning", "Other"])

        if st.button("Add Habit"):
            if new_habit:
                dm.add_habit(new_habit, habit_category)
                st.success(f"Added habit: {new_habit}")
                st.session_state.habits_data = dm.load_habits_data()
            else:
                st.error("Please enter a habit name")

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Today's Habits")
        habits_df = st.session_state.habits_data

        if not habits_df.empty:
            for _, habit in habits_df.iterrows():
                habit_name = habit['habit_name']
                completed = st.checkbox(
                    habit_name,
                    value=dm.is_habit_completed_today(habit_name),
                    key=f"check_{habit_name}"
                )
                if completed:
                    dm.mark_habit_complete(habit_name)
                else:
                    dm.mark_habit_incomplete(habit_name)
        else:
            st.info("No habits added yet. Add some habits using the sidebar!")

    with col2:
        st.subheader("Statistics")
        if not habits_df.empty:
            total_habits = len(habits_df)
            completed_today = dm.get_completed_habits_count_today()
            st.metric("Total Habits", total_habits)
            st.metric("Completed Today", completed_today)

    # Visualizations
    if not habits_df.empty:
        st.subheader("Progress Visualization")
        tab1, tab2 = st.tabs(["Streak Calendar", "Completion Rate"])

        with tab1:
            calendar_data = viz.generate_calendar_data()
            fig_calendar = viz.plot_calendar_heatmap(calendar_data)
            st.plotly_chart(fig_calendar, use_container_width=True)

        with tab2:
            completion_data = viz.generate_completion_data()
            fig_completion = viz.plot_completion_rate(completion_data)
            st.plotly_chart(fig_completion, use_container_width=True)

if __name__ == "__main__":
    main()