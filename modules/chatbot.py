# modules/chatbot.py

import streamlit as st
from modules.chatlogic import get_bot_response

def process_chatbot_mode():
   
    st.title("💬 Chatbot")
    st.write("Ask me about **jobs**, **internships**, **skills**, or **courses** for any tech role!")

    with st.form("chat_form"):
        user_input = st.text_input("Type your query here:", placeholder="e.g., jobs for data analyst")
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        with st.spinner("Finding the best resources..."):
            response = get_bot_response(user_input)

        st.markdown("### 📢 Bot Response:")
        st.markdown(response, unsafe_allow_html=True)
