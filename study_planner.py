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
        
    # Study Calendar Section
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
            
    # Motivation Box
    st.subheader("Need Motivation?")
    if st.button("Get Motivated! 💪"):
        motivation = get_motivation_message()
        st.info(motivation, icon="✨")
    
    # Goal Setting Section
    st.subheader("Study Goals")
    new_goal = st.text_input("Set a New Goal")
    if st.button("Add Goal"):
        if new_goal:
            if 'study_goals' not in st.session_state:
                st.session_state.study_goals = []
            st.session_state.study_goals.append(new_goal)
            st.success("Goal added successfully!")
    
    if 'study_goals' in st.session_state and st.session_state.study_goals:
        st.write("Your Goals:")
        for i, goal in enumerate(st.session_state.study_goals, 1):
            st.write(f"{i}. 🎯 {goal}")
