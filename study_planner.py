import streamlit as st
import pandas as pd
from datetime import datetime
import random
from models import db, User
from app import app

def get_motivation_message():
    messages = [
        "Start with just 5 minutes!",
        "Done is better than perfect!",
        "Break tasks into small steps!",
        "You've got this!",
        "Progress over perfection!",
        "Every minute counts!"
    ]
    return random.choice(messages)

def study_planner_page():
    st.title("📚 Study Planner")

    if not st.session_state.authenticated:
        st.warning("Please login to access the Study Planner")
        return

    # Custom CSS for pink theme
    st.markdown("""
        <style>
        .main {
            background-color: #ffebf2;
        }
        .stButton>button {
            background-color: white;
            color: #333;
            border: 1px solid #ff69b4;
        }
        .stButton>button:hover {
            background-color: #ff69b4;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    # Navigation tabs
    tab1, tab2, tab3 = st.tabs(["📝 Study Tasks", "✍️ Journaling", "🎯 Pomodoro"])

    with tab1:
        st.subheader("Study Calendar")
        col1, col2 = st.columns([2, 1])

        with col1:
            study_date = st.date_input("Select Date", datetime.now())
            study_task = st.text_input("Study Task")

            if st.button("Add Task"):
                if study_task:
                    if 'study_tasks' not in st.session_state:
                        st.session_state.study_tasks = []
                    st.session_state.study_tasks.append({
                        'date': study_date.strftime('%Y-%m-%d'),
                        'task': study_task
                    })
                    st.success("Task added successfully!")

        # Display tasks
        if 'study_tasks' in st.session_state and st.session_state.study_tasks:
            st.subheader("Your Study Tasks")
            for task in st.session_state.study_tasks:
                st.write(f"📅 {task['date']}: {task['task']}")

    with tab2:
        st.subheader("Study Journal")
        journal_entry = st.text_area("Today's Study Reflection", 
            placeholder="Reflect on your study session...\n- What did you learn?\n- What challenges did you face?\n- What will you focus on next?")

        if st.button("Save Journal Entry"):
            if journal_entry:
                if 'journal_entries' not in st.session_state:
                    st.session_state.journal_entries = []
                st.session_state.journal_entries.append({
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'entry': journal_entry
                })
                st.success("Journal entry saved!")

        if 'journal_entries' in st.session_state and st.session_state.journal_entries:
            st.subheader("Previous Entries")
            for entry in reversed(st.session_state.journal_entries):
                with st.expander(f"Entry from {entry['date']}"):
                    st.write(entry['entry'])

    with tab3:
        st.subheader("Pomodoro Timer")
        col1, col2 = st.columns([2, 1])

        with col1:
            if 'timer_running' not in st.session_state:
                st.session_state.timer_running = False
            if 'time_remaining' not in st.session_state:
                st.session_state.time_remaining = 25 * 60  # 25 minutes in seconds

            minutes = st.slider("Study Duration (minutes)", 5, 60, 25)

            if st.button("Start Timer" if not st.session_state.timer_running else "Stop Timer"):
                st.session_state.timer_running = not st.session_state.timer_running
                st.session_state.time_remaining = minutes * 60
                st.rerun()

        with col2:
            # Motivation Box
            st.info(get_motivation_message(), icon="✨")