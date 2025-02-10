import streamlit as st

def apply_styles():
    """Apply custom styles to the application"""
    st.markdown("""
        <style>
        .stCheckbox {
            font-size: 1.2rem;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 5px;
            margin: 5px 0;
        }
        .stCheckbox:hover {
            background-color: #e9ecef;
        }
        .stMetric {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .stTitle {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 2rem;
        }
        .stSubheader {
            font-size: 1.8rem;
            margin: 1rem 0;
        }
        .sidebar .stButton button {
            width: 100%;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
