import streamlit as st

st.sidebar.title("RAG System")
choice = st.sidebar.selectbox("Menu", ["Upload", "Chat"])

if choice == "Upload":
    import frontend.rag_upload_app
if choice == "Chat":
    import frontend.rag_chat_app
