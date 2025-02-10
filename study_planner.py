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

    # Custom CSS for pink theme with rounded corners
    st.markdown("""
        <style>
        .main {
            background-color: #ffebf2;
        }
        .stButton>button {
            background-color: white;
            color: #333;
            border: 1px solid #ff69b4;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #ff69b4;
            color: white;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
        }
        .stTextArea>div>div>textarea {
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Navigation tabs with emojis
    tab1, tab2, tab3 = st.tabs([
        "📅 Schedule", 
        "✅ To-Do List", 
        "⏱️ Study Timer"
    ])

    with tab1:
        st.subheader("Study Schedule")
        col1, col2 = st.columns([2, 1])

        with col1:
            study_date = st.date_input("Select Date", datetime.now())
            study_task = st.text_input("Study Task")
            duration = st.number_input("Duration (minutes)", min_value=15, max_value=180, value=30, step=15)

            if st.button("Add to Schedule"):
                if study_task:
                    if 'study_schedule' not in st.session_state:
                        st.session_state.study_schedule = []
                    st.session_state.study_schedule.append({
                        'date': study_date.strftime('%Y-%m-%d'),
                        'task': study_task,
                        'duration': duration
                    })
                    st.success("Task scheduled successfully!")

        # Display schedule
        if 'study_schedule' in st.session_state and st.session_state.study_schedule:
            st.subheader("Your Schedule")
            for task in st.session_state.study_schedule:
                st.info(f"📅 {task['date']}: {task['task']} ({task['duration']} minutes)")

    with tab2:
        st.subheader("To-Do List")
        new_todo = st.text_input("New Task")
        priority = st.select_slider("Priority", options=["Low", "Medium", "High"], value="Medium")

        if st.button("Add Task"):
            if new_todo:
                if 'todos' not in st.session_state:
                    st.session_state.todos = []
                st.session_state.todos.append({
                    'task': new_todo,
                    'priority': priority,
                    'completed': False
                })
                st.success("Task added!")

        if 'todos' in st.session_state and st.session_state.todos:
            for i, todo in enumerate(st.session_state.todos):
                col1, col2 = st.columns([3, 1])
                with col1:
                    done = st.checkbox(
                        todo['task'],
                        value=todo['completed'],
                        key=f"todo_{i}"
                    )
                    if done != todo['completed']:
                        st.session_state.todos[i]['completed'] = done
                with col2:
                    st.markdown(f"Priority: **{todo['priority']}**")

    with tab3:
        st.subheader("Study Timer")
        
        if 'timer_running' not in st.session_state:
            st.session_state.timer_running = False
        if 'time_remaining' not in st.session_state:
            st.session_state.time_remaining = 25 * 60

        if st.session_state.timer_running:
            # Full screen timer mode
            st.markdown("""
                <style>
                .big-timer {
                    font-size: 120px;
                    text-align: center;
                    margin: 50px 0;
                }
                </style>
            """, unsafe_allow_html=True)
            
            minutes = st.session_state.time_remaining // 60
            seconds = st.session_state.time_remaining % 60
            st.markdown(f"<div class='big-timer'>{minutes:02d}:{seconds:02d}</div>", unsafe_allow_html=True)
            
            if st.button("Stop Timer", use_container_width=True):
                st.session_state.timer_running = False
                st.rerun()
            
            # Motivation message in timer mode
            st.markdown("---")
            st.info(get_motivation_message(), icon="✨")
            
        else:
            # Timer setup mode
            col1, col2 = st.columns([2, 1])
            
            with col1:
                timer_options = {
                    "Short Session": 15,
                    "Standard Session": 25,
                    "Long Session": 45,
                    "Custom": 0
                }

                session_type = st.radio("Session Type", list(timer_options.keys()))

                if session_type == "Custom":
                    minutes = st.slider("Custom Duration (minutes)", 5, 60, 25)
                else:
                    minutes = timer_options[session_type]

                if st.button("Start Timer", use_container_width=True):
                    st.session_state.timer_running = True
                    st.session_state.time_remaining = minutes * 60
                    st.rerun()

            with col2:
                # Motivation Box
                st.info(get_motivation_message(), icon="✨")