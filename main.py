# main.py
import streamlit as st
from modules.home import show_home
from modules.login import show_login
from modules.profile import show_profile
from modules.users import process_user_mode
from modules.recruiters import process_recruiters_mode
from modules.admin import process_admin_mode
from modules.feedback import process_feedback_mode
from modules.chatbot import process_chatbot_mode
from modules.dashboard import show_dashboard
def main():
    st.set_page_config(page_title="Resume Parser", page_icon="✅")

    # Sidebar
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose an option", ["Home","Login","Profile","Users", "Recruiters", "Feedback", "Admin", "Chatbot","DashBoard"])

    if app_mode == "Home":
        show_home()
    elif app_mode=="Login":
        show_login()
    elif app_mode=="Profile":
        show_profile()

    elif app_mode == "Users":
        process_user_mode()

    elif app_mode == "Recruiters":
        process_recruiters_mode()

    elif app_mode == "Admin":
        process_admin_mode()

    elif app_mode == "Feedback":
        process_feedback_mode()

    elif app_mode == "Chatbot":
        process_chatbot_mode()
        
    elif app_mode == "DashBoard":
        show_dashboard()

if __name__ == "__main__":
    main()
