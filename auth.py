import streamlit as st
from models import User, db
import re
from app import app

def is_valid_email(email):
    """Check if email is valid"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def login_page():
    st.title("Welcome to UnStuck")
    st.title("Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if not email or not password:
                st.error("Please enter both email and password")
                return

            with app.app_context():
                user = User.query.filter_by(email=email).first()
                if user and user.check_password(password):
                    st.session_state.authenticated = True
                    st.session_state.user_id = user.id
                    st.session_state.user_email = user.email
                    st.session_state.first_name = user.first_name
                    st.session_state.current_page = "login"  # This will show welcome page
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")

    # Navigation button
    if st.button("Don't have an account? Sign up"):
        st.query_params["page"] = "signup"
        st.rerun()

def signup_page():
    st.title("Sign Up")

    with st.form("signup_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")

        if submit:
            if not first_name or not last_name or not email or not password or not password_confirm:
                st.error("Please fill in all fields")
                return

            if not is_valid_email(email):
                st.error("Please enter a valid email address")
                return

            if password != password_confirm:
                st.error("Passwords don't match")
                return

            with app.app_context():
                if User.query.filter_by(email=email).first():
                    st.error("Email already registered")
                    return

                user = User(email=email, first_name=first_name, last_name=last_name)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()

                st.session_state.authenticated = True
                st.session_state.user_id = user.id
                st.session_state.user_email = user.email
                st.session_state.current_page = "login"  # This will show welcome page
                st.success("Account created successfully!")
                st.rerun()

    # Navigation button
    if st.button("Already have an account? Login"):
        st.query_params["page"] = "login"
        st.rerun()