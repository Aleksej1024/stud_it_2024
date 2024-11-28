from streamlit_pdf_viewer import pdf_viewer
import streamlit as st

container_pdf, container_chat = st.columns([50, 50])

st.title("Инструкция")
with open("./Руководство пользователя.pdf","r") as f:
    pdf_viewer("./Руководство пользователя.pdf")
