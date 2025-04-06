import streamlit as st
import psycopg2

# Database connection function
def connect_db():
    return psycopg2.connect(
        dbname="skillsync",
        user="postgres",  # Change if needed
        password="123456789",  # Replace with actual password
        host="localhost",
        port="5432"
    )

# Function to fetch user profile using username
def get_user_profile(username):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT age, email, education, interest, skills FROM user_profiles WHERE username = %s", (username,))
    user_data = cur.fetchone()
    cur.close()
    conn.close()
    return user_data

# Function to insert or update profile in user_profiles
def update_user_profile(username, age, email, education, interest, skills):
    conn = connect_db()
    cur = conn.cursor()

    # Check if profile exists
    cur.execute("SELECT username FROM user_profiles WHERE username = %s", (username,))
    if cur.fetchone():
        # Update existing profile
        cur.execute("""
            UPDATE user_profiles 
            SET age = %s, email = %s, education = %s, interest = %s, skills = %s 
            WHERE username = %s
        """, (age, email, education, interest, skills, username))
    else:
        # Insert new profile
        cur.execute("""
            INSERT INTO user_profiles (username, age, email, education, interest, skills)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, age, email, education, interest, skills))

    conn.commit()
    cur.close()
    conn.close()

# Streamlit UI - Load HTML and Handle Profile Update
def show_profile():
    st.title("My Profile")

    # Load HTML file
    with open("frontend/profile.html", "r", encoding="utf-8") as file:
        profile_html = file.read()

    # Display HTML form
    st.components.v1.html(profile_html, height=900, scrolling=True)

    # Username input to fetch details
    username = st.text_input("Enter your Username:")

    if st.button("Fetch Profile"):
        user_data = get_user_profile(username)
        if user_data:
            st.session_state["age"], st.session_state["email"], st.session_state["education"], st.session_state["interest"], st.session_state["skills"] = user_data
            st.success("Profile fetched successfully!")
        else:
            st.warning("No profile found. Please fill in your details.")

    # Profile Update Form
    with st.form(key="profile_form"):
        age = st.number_input("Age", min_value=0, step=1, value=st.session_state.get("age", 18))
        email = st.text_input("Email", st.session_state.get("email", ""))
        education = st.text_input("Education", st.session_state.get("education", ""))
        interest = st.text_input("Area of Interest", st.session_state.get("interest", ""))
        skills = st.text_input("Skills (comma-separated)", st.session_state.get("skills", ""))

        if st.form_submit_button("Save Profile"):
            update_user_profile(username, age, email, education, interest, skills)
            st.success("Profile Updated Successfully!")

