import streamlit as st
from models import User, db
import re

def is_valid_email(email):
    """Check if email is valid"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def login_page():
    st.title("Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if not email or not password:
                st.error("Please enter both email and password")
                return

            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                st.session_state.authenticated = True
                st.session_state.user_id = user.id
                st.success("Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("Invalid email or password")

    # Navigation button instead of markdown link
    if st.button("Don't have an account? Sign up"):
        st.experimental_set_query_params(page="signup")
        st.experimental_rerun()

def signup_page():
    st.title("Sign Up")

    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")

        if submit:
            if not email or not password or not password_confirm:
                st.error("Please fill in all fields")
                return

            if not is_valid_email(email):
                st.error("Please enter a valid email address")
                return

            if password != password_confirm:
                st.error("Passwords don't match")
                return

            if User.query.filter_by(email=email).first():
                st.error("Email already registered")
                return

            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            st.session_state.authenticated = True
            st.session_state.user_id = user.id
            st.success("Account created successfully!")
            st.experimental_rerun()

    # Navigation button instead of markdown link
    if st.button("Already have an account? Login"):
        st.experimental_set_query_params(page="login")
        st.experimental_rerun()