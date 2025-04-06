import streamlit as st
import psycopg2
from datetime import datetime

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

# Function to insert feedback into PostgreSQL
def add_feedback(user_name, feedback):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "INSERT INTO feedback (user_name, feedback) VALUES (%s, %s)"
        cursor.execute(query, (user_name, feedback))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Feedback submitted successfully!")
    except Exception as e:
        st.error(f"Error submitting feedback: {e}")

# Streamlit UI
def process_feedback_mode():
    st.title("Feedback Section")
    st.subheader("Provide Feedback")

    # Feedback Form
    user_name = st.text_input("Your Name:")
    feedback = st.text_area("Provide feedback on the resume parser:", height=100)

    if st.button("Submit Feedback"):
        if user_name and feedback:
            add_feedback(user_name, feedback)
        else:
            st.warning("Please fill in all fields before submitting.")

