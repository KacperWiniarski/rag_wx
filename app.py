import streamlit as st
from frontend import rag_upload_app, rag_chat_app

st.sidebar.title("RAG System")
choice = st.sidebar.selectbox("Menu", ["Upload", "Chat"])

if choice == "Upload":
    rag_upload_app.app()
elif choice == "Chat":
    rag_chat_app.app()
