import streamlit as st
from retrieval.rag_pipeline import rag_answer

def app():
    st.title("💬 RAG Chat")
    
    # Inicjalizacja historii czatu w session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Wyświetlanie historii czatu
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Input użytkownika
    user_input = st.chat_input("Zadaj pytanie:")
    
    if user_input:
        # Dodaj pytanie użytkownika do historii
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Wyświetl pytanie użytkownika
        with st.chat_message("user"):
            st.write(user_input)
        
        # Generuj odpowiedź z historią (maksymalnie 3 pytania wstecz)
        with st.chat_message("assistant"):
            with st.spinner("Myślę..."):
                response = rag_answer(user_input, st.session_state.chat_history)
                st.write(response)
        
        # Dodaj odpowiedź do historii
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
    
    # Przycisk do czyszczenia historii
    if st.session_state.chat_history:
        if st.button("🗑️ Wyczyść historię czatu"):
            st.session_state.chat_history = []
            st.rerun()
