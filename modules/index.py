import streamlit as st

def show_index():
    st.title("Index Page")

    with open("frontend/index.html", "r", encoding="utf-8") as file:
        index_html = file.read()

    st.components.v1.html(index_html, height=700, scrolling=True)
