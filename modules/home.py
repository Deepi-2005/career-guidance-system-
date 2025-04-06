import streamlit as st

def show_home():

    with open("frontend/home.html", "r", encoding="utf-8") as file:
        home_html = file.read()

    st.components.v1.html(home_html, height=900, scrolling=True)
