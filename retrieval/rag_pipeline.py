from config.watsonx_config import get_llm_model
from retrieval.retriever import search
import re


llm_model = get_llm_model()


def remove_repetitions(text):
    """Usuwa powtarzające się zdania z odpowiedzi."""
    sentences = text.split('.')
    seen = set()
    result = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and sentence not in seen:
            seen.add(sentence)
            result.append(sentence)
    
    return '. '.join(result) + ('.' if result and not text.endswith('.') else '')


def rag_answer(question, chat_history=None):
    """
    Generate an answer to a question using RAG (Retrieval-Augmented Generation) with conversation history.
    
    Args:
        question (str): The user's current question
        chat_history (list, optional): List of previous messages [{"role": "user/assistant", "content": "..."}]
        
    Returns:
        str: The generated answer based on retrieved context and conversation history
    """
    # Retrieve context from the retriever
    context_chunks = search(question)
    context = "\n".join(context_chunks)
    
    # Build conversation history string (maksymalnie 3 pytania wstecz = 6 wiadomości: 3 pytania + 3 odpowiedzi)
    history_text = ""
    if chat_history and len(chat_history) > 1:
        # Bierzemy ostatnie 6 wiadomości (3 pary pytanie-odpowiedź), pomijając aktualną wiadomość
        max_history_messages = 6
        recent_history = chat_history[-(max_history_messages + 1):-1] if len(chat_history) > max_history_messages else chat_history[:-1]
        
        if recent_history:
            history_text = "\n".join([
                f"{'Użytkownik' if msg['role'] == 'user' else 'Asystent'}: {msg['content']}"
                for msg in recent_history
            ])

    # Prepare prompt with history
    prompt = f"""Jesteś asystentem AI. Odpowiadaj zwięźle po polsku, bazując TYLKO na kontekście.

{f"Historia:\n{history_text}\n\n" if history_text else ""}Kontekst:
{context}

Pytanie: {question}

Odpowiedź (krótka, bez powtórzeń):"""

    # Call LLM using the initialized model
    response = llm_model(prompt)
    
    # Post-processing: usuń powtórzenia
    response = remove_repetitions(response)
    
    # Obetnij po pierwszym "Pozdrawiam" jeśli występuje wielokrotnie
    if response.count("Pozdrawiam") > 1:
        first_pozdrawiam = response.find("Pozdrawiam")
        response = response[:first_pozdrawiam + len("Pozdrawiam") + 1]
    
    return response.strip()
