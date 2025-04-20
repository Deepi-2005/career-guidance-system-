import streamlit as st
import psycopg2
import plotly.graph_objects as go

# ------------------- Database Connection -------------------
def connect_db():
    return psycopg2.connect(
        dbname="skillsync",
        user="postgres",
        password="123456789",
        host="localhost",
        port="5432"
    )

# ------------------- Fetch User Profile -------------------
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

# ------------------- Predefined Skills by Role -------------------
role_required_skills = {
    "Data Scientist": {"python", "machine learning", "data visualization", "pandas", "numpy"},
    "Frontend Developer": {"html", "css", "javascript", "react", "git"},
    "Backend Developer": {"java", "sql", "spring", "api", "docker"},
    "Full Stack Developer": {"html", "css", "javascript", "python", "sql", "react", "nodejs"},
}

# ------------------- Suggest Skills for Role -------------------
def suggest_skills_for_job(job_role):
    return list(role_required_skills.get(job_role.title(), []))

# ------------------- Analyze Skill Gap -------------------
def analyze_skill_gap(resume_skills, desired_job):
    suggested_skills = suggest_skills_for_job(desired_job)

    resume_skills_set = set(skill.lower() for skill in resume_skills)
    suggested_skills_set = set(skill.lower() for skill in suggested_skills)

    matched_skills = resume_skills_set.intersection(suggested_skills_set)
    missing_skills = suggested_skills_set.difference(resume_skills_set)

    match_score = int((len(matched_skills) / len(suggested_skills_set)) * 100) if suggested_skills_set else 0

    return {
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "match_score": match_score,
        "required_skills": list(suggested_skills_set)
    }

# ------------------- Format Skill Badge -------------------
def format_badge(text, color):
    return f"<span style='background-color:{color}; padding:4px 10px; border-radius:12px; margin:2px; display:inline-block; color:white'>{text}</span>"

# ------------------- Placeholder for Resume Parser -------------------
def extract_resume_info(doc=None):
    return {
        "first_name": "Deepika",
        "last_name": "S",
        "email": "deepika@example.com",
        "degree_major": "Computer Science",
        "skills": ["python", "sql", "html", "css", "javascript"]
    }

# ------------------- Calculate Resume Score -------------------
def calculate_resume_score(resume_info, desired_job=None):
    score = 0
    if resume_info['first_name'] and resume_info['last_name']:
        score += 20
    if resume_info['email']:
        score += 20
    if resume_info['degree_major']:
        score += 20
    if resume_info['skills']:
        score += 20

    if desired_job:
        gap_analysis = analyze_skill_gap(resume_info['skills'], desired_job)
        score += int(gap_analysis["match_score"] * 0.2)

    return score

# ------------------- Dashboard -------------------
def show_dashboard():
    st.title("🎯 Career Dashboard")

    username = st.text_input("Enter your Username to Load Dashboard:")

    if st.button("Load My Dashboard"):
        profile = get_user_profile(username)

        if profile:
            age, email, education, interest, skills, resume_filename, target_role, skills_updated = profile
            skills = skills.split(",")  # Assuming comma-separated string in DB

            st.subheader("👤 User Profile")
            st.markdown(f"""
            - **Age:** {age}  
            - **Email:** {email}  
            - **Education:** {education}  
            - **Interest:** {interest}  
            - **Target Role:** {target_role}  
            - **Skills Updated:** {"✅ Yes" if skills_updated else "❌ No"}  
            - **Uploaded Resume:** {resume_filename if resume_filename else 'Not uploaded'}
            """)
            st.divider()

            # Skill Gap Analysis
            st.subheader("📊 Skill Gap Analysis")
            gap = analyze_skill_gap(skills, target_role)
            matched = gap["matched_skills"]
            missing = gap["missing_skills"]
            required = gap["required_skills"]
            match_percent = gap["match_score"]

            st.markdown("**✅ Matched Skills:**", unsafe_allow_html=True)
            st.markdown("".join([format_badge(skill, "#4CAF50") for skill in matched]), unsafe_allow_html=True)

            st.markdown("**❌ Missing Skills:**", unsafe_allow_html=True)
            st.markdown("".join([format_badge(skill, "#F44336") for skill in missing]), unsafe_allow_html=True)

            st.markdown("**📌 Required Skills:**", unsafe_allow_html=True)
            st.markdown("".join([format_badge(skill, "#2196F3") for skill in required]), unsafe_allow_html=True)

            st.divider()
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader("📈 Progress Tracker")
                st.progress(match_percent / 100)
            with col2:
                st.metric("Skill Match Score", f"{match_percent}%", delta=f"{match_percent - 50}%")

            if match_percent == 100:
                st.success("🎉 You are fully prepared for your target role!")
            elif match_percent >= 70:
                st.info("💪 You're almost there! Just a few more skills to learn.")
            elif match_percent >= 40:
                st.warning("🚧 You need to improve on several important skills.")
            else:
                st.error("⚠️ Significant gap. Start upskilling today!")

            if missing:
                st.subheader("📚 Suggestions to Improve:")
                for skill in missing:
                    st.markdown(f"""
                    <div style='margin-bottom:10px'>
                    📌 <b>{skill.title()}</b><br>
                    🔗 <a href='https://www.coursera.org/search?query={skill}' target='_blank'>Coursera</a> | 
                    <a href='https://www.udemy.com/courses/search/?q={skill}' target='_blank'>Udemy</a> | 
                    <a href='https://www.youtube.com/results?search_query=learn+{skill}' target='_blank'>YouTube</a>
                    </div>
                    """, unsafe_allow_html=True)

            st.divider()
            st.subheader("📊 Visual Skill Match")
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=[1 if skill in matched else 0 for skill in required],
                theta=list(required),
                fill='toself',
                name='Your Skill Coverage',
                line_color='green'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("User not found. Please check the username.")

# ------------------- Run App -------------------
if __name__ == "__main__":
    show_dashboard()
