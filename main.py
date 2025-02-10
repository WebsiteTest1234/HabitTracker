import streamlit as st
import pandas as pd
from datetime import datetime
import utils
import data_manager as dm
import visualizations as viz
from styles import apply_styles
from auth import login_page, signup_page
from app import app, init_db
from study_planner import study_planner_page
from models import User

def welcome_page():
    st.title(f"Welcome {st.session_state.user_email}! 👋")

    st.subheader("What do you need help with today?")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Habit Tracker", use_container_width=True):
            st.session_state.current_page = "Habit Tracker"
            st.rerun()

    with col2:
        if st.button("📚 Study Planner", use_container_width=True):
            st.session_state.current_page = "Study Planner"
            st.rerun()

    with col3:
        if st.button("✍️ Journaling", use_container_width=True):
            st.session_state.current_page = "Journaling"
            st.rerun()

def main():
    st.set_page_config(page_title="Habit & Study Tracker", layout="wide")
    apply_styles()

    # Initialize database within app context
    with app.app_context():
        error = init_db()
        if error:
            st.error(f"Error initializing database: {error}")
            return

    # Session state initialization
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "login"

    # Check if user is authenticated
    if not st.session_state.authenticated:
        # Query parameters for login/signup navigation
        params = st.query_params
        page = params.get("page", "login")

        if page == "signup":
            signup_page()
        else:
            login_page()
        return

    # Show logout button in sidebar
    with st.sidebar:
        st.title("Navigation")
        if st.button("🚪 Logout", key="logout_button"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.session_state.current_page = "login"
            st.rerun()

    # Display selected page
    if st.session_state.current_page == "login":
        welcome_page()
    elif st.session_state.current_page == "Study Planner":
        study_planner_page()
    elif st.session_state.current_page == "Journaling":
        st.title("✍️ Journaling")
        # Journaling content will be added later
        st.info("Journaling feature coming soon!")
    else:
        # Habit Tracker page
        st.title("🎯 Habit Tracker")

        if 'habits_data' not in st.session_state:
            st.session_state.habits_data = dm.load_habits_data()

        # Sidebar for adding new habits
        with st.sidebar:
            st.header("Add New Habit")
            new_habit = st.text_input("Habit Name", key="new_habit_input")
            habit_category = st.selectbox(
                "Category",
                ["Health", "Productivity", "Learning", "Other"],
                key="category_select"
            )

            if st.button("Add Habit", key="add_habit_button"):
                if new_habit:
                    with app.app_context():
                        dm.add_habit(new_habit, habit_category)
                    st.success(f"Added habit: {new_habit}")
                    st.session_state.habits_data = dm.load_habits_data()
                    st.rerun()
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
                    with app.app_context():
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
                with app.app_context():
                    total_habits = len(habits_df)
                    completed_today = dm.get_completed_habits_count_today()
                    st.metric("Total Habits", total_habits)
                    st.metric("Completed Today", completed_today)

        # Visualizations
        if not habits_df.empty:
            st.subheader("Progress Visualization")
            tab1, tab2 = st.tabs(["Streak Calendar", "Completion Rate"])

            with tab1:
                with app.app_context():
                    calendar_data = viz.generate_calendar_data()
                    fig_calendar = viz.plot_calendar_heatmap(calendar_data)
                    st.plotly_chart(fig_calendar, use_container_width=True)

            with tab2:
                with app.app_context():
                    completion_data = viz.generate_completion_data()
                    fig_completion = viz.plot_completion_rate(completion_data)
                    st.plotly_chart(fig_completion, use_container_width=True)

if __name__ == "__main__":
    main()