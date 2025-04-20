import streamlit as st
import psycopg2

# Database connection function
def connect_db():
    return psycopg2.connect(
        dbname="skillsync",
        user="postgres",
        password="123456789",
        host="localhost",
        port="5432"
    )

# Fetch complete profile
def get_user_profile(username):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT age, email, education, interest, skills, resume_filename, target_role, skills_updated 
        FROM user_profiles 
        WHERE username = %s
    """, (username,))
    user_data = cur.fetchone()
    cur.close()
    conn.close()
    return user_data

# Insert or update profile
def update_user_profile(username, age, email, education, interest, skills,
                        resume_file, resume_filename, target_role, skills_updated):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT username FROM user_profiles WHERE username = %s", (username,))
    if cur.fetchone():
        cur.execute("""
            UPDATE user_profiles 
            SET age = %s, email = %s, education = %s, interest = %s, skills = %s,
                resume_file = %s, resume_filename = %s, target_role = %s, skills_updated = %s
            WHERE username = %s
        """, (age, email, education, interest, skills,
              resume_file, resume_filename, target_role, skills_updated, username))
    else:
        cur.execute("""
            INSERT INTO user_profiles 
            (username, age, email, education, interest, skills, resume_file, resume_filename,
             target_role, skills_updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (username, age, email, education, interest, skills, resume_file, resume_filename,
              target_role, skills_updated))

    conn.commit()
    cur.close()
    conn.close()

# Streamlit UI
def show_profile():
    st.title("My Profile")

    username = st.text_input("Enter your Username:")

    if st.button("Fetch Profile"):
        user_data = get_user_profile(username)
        if user_data:
            (
                st.session_state["age"],
                st.session_state["email"],
                st.session_state["education"],
                st.session_state["interest"],
                st.session_state["skills"],
                st.session_state["resume_filename"],
                st.session_state["target_role"],
                st.session_state["skills_updated"]
            ) = user_data
            st.success("Profile fetched successfully!")
        else:
            st.warning("No profile found. Please fill in your details.")

    with st.form(key="profile_form"):
        age = st.number_input("Age", min_value=0, step=1, value=st.session_state.get("age", 18))
        email = st.text_input("Email", st.session_state.get("email", ""))
        education = st.text_input("Education", st.session_state.get("education", ""))
        interest = st.text_input("Area of Interest", st.session_state.get("interest", ""))
        skills = st.text_input("Skills (comma-separated)", st.session_state.get("skills", ""))
        target_role = st.text_input("Target Job Role", st.session_state.get("target_role", ""))
        skills_updated = st.checkbox("Skills Updated", st.session_state.get("skills_updated", False))

        # Resume Upload
        resume_uploaded = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])
        resume_file = None
        resume_filename = None
        if resume_uploaded is not None:
            resume_file = resume_uploaded.read()
            resume_filename = resume_uploaded.name

        if st.form_submit_button("Save Profile"):
            update_user_profile(username, age, email, education, interest, skills,
                                resume_file, resume_filename, target_role, skills_updated)
            st.success("Profile Updated Successfully!")

# Run the app
if __name__ == "__main__":
    show_profile()
