# modules/chatbot.py
import streamlit as st
from modules.chatlogic import get_bot_response

def process_chatbot_mode():
    st.title("💬 SkillSync Chatbot")
    st.write("Ask me anything about job roles, skills, or resumes!")

    user_input = st.text_input("You:", key="chat_input")

    if user_input:
        response = get_bot_response(user_input)
        st.markdown(f"**Bot:** {response}")
