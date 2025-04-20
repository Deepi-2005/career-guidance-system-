import streamlit as st
import psycopg2
import hashlib
from modules.dashboard import show_dashboard  # Create this file for Dashboard page

# Database connection details
DB_NAME = "skillsync"
DB_USER = "postgres"
DB_PASSWORD = "123456789"
DB_HOST = "localhost"
DB_PORT = "5432"

def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def verify_user(username, password):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, hashed_password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user is not None
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def show_login():
    st.title("Login Page")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if verify_user(username, password):
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.username = username  # store username in session
                st.experimental_rerun()  # refresh page to go to dashboard
            else:
                st.error("Invalid Username or Password")

    if st.session_state.logged_in:
        show_dashboard()  # Call your dashboard page here

