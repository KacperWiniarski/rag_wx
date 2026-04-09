import streamlit as st
from retrieval.rag_pipeline import rag_answer

def app():
    st.title("💬 RAG Chat")
    
    user_input = st.text_input("Zadaj pytanie:")
    
    if user_input:
        response = rag_answer(user_input)
        st.write(response)
