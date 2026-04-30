from config.watsonx_config import get_llm_model
from retrieval.retriever import search
import re


llm_model = get_llm_model()


def clean_response(text):
    """Czyści odpowiedź z niepotrzebnych dodatków i powtórzeń."""
    # Usuń powtarzające się zdania
    sentences = text.split('.')
    seen = set()
    result = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and sentence not in seen:
            seen.add(sentence)
            result.append(sentence)
    
    cleaned = '. '.join(result)
    
    # Obetnij po pierwszym zdaniu jeśli zawiera kompletną odpowiedź
    # (np. "FN." lub "Symbol to FN.")
    first_sentence = result[0] if result else ""
    
    # Jeśli pierwsze zdanie jest krótkie i zawiera odpowiedź, zwróć tylko je
    if len(first_sentence) < 100 and any(keyword in first_sentence.lower() for keyword in ['symbol', 'to', 'jest', 'wynosi', 'ma']):
        return first_sentence + '.'
    
    # Obetnij po znakach sugerujących koniec odpowiedzi
    for stop_phrase in ['Inna forma', 'Może być', 'itp.', 'np.', 'Pozdrawiam', 'Dziękuję']:
        if stop_phrase in cleaned:
            cleaned = cleaned[:cleaned.find(stop_phrase)].strip()
            break
    
    return cleaned + ('.' if cleaned and not cleaned.endswith('.') else '')


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
    
    # Post-processing: wyczyść odpowiedź
    response = clean_response(response)
    
    return response.strip()
