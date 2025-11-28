import streamlit as st
from retrieval.rag_pipeline import rag_answer

st.title("💬 RAG Chat")

question = st.text_input("Ask something:")

if st.button("Send"):
    answer = rag_answer(question)
    st.write(answer)
