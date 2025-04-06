import streamlit as st
import psycopg2
import hashlib
import json
from streamlit.components.v1 import html

# Database connection details
DB_NAME = "skillsync"
DB_USER = "postgres"
DB_PASSWORD = "123456789"  # Replace with your actual password
DB_HOST = "localhost"
DB_PORT = "5432"

# Function to connect to PostgreSQL
def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# Function to verify user login
def verify_user(username, password):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Hash the entered password to match stored passwords
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, hashed_password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user is not None  # Returns True if user exists, False otherwise

    except Exception as e:
        return {"message": f"Database error: {e}"}

# Streamlit Login Page
def show_login():
    st.title("Login Page")

    # Load HTML
    with open("frontend/login.html", "r", encoding="utf-8") as file:
        login_html = file.read()

    # Embed HTML
    html(login_html, height=700, scrolling=True)

    # Handle login request
    def handle_login():
        try:
            # Read JSON data from frontend
            request_data = json.loads(st.experimental_get_query_params().get("data", "{}"))
            username = request_data.get("username")
            password = request_data.get("password")

            if username and password:
                if verify_user(username, password):
                    return json.dumps({"message": "Login successful! ✅"})
                else:
                    return json.dumps({"message": "Invalid username or password ❌"})
            else:
                return json.dumps({"message": "Please enter both username and password."})
        except Exception as e:
            return json.dumps({"message": f"Error processing request: {e}"})

    # Check if login request is received
    if "data" in st.experimental_get_query_params():
        st.write(handle_login())


