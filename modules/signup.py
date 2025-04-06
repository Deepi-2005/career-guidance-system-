import streamlit as st

def show_login():
    st.title("Signup Page")

    with open("frontend/signup.html", "r", encoding="utf-8") as file:
        login_html = file.read()

    st.components.v1.html(signup_html, height=700, scrolling=True)
