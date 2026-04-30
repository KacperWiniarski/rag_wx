from config.watsonx_config import get_llm_model
from retrieval.retriever import search


llm_model = get_llm_model()


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
    prompt = f"""Jesteś asystentem AI wspierającym użytkowników. Odpowiadaj tylko po polsku i tylko na bazie kontekstu.

{f"Historia ostatnich 3 pytań:\n{history_text}\n\n" if history_text else ""}Kontekst z bazy wiedzy:
{context}

Aktualne pytanie: {question}

Instrukcje:
- Odpowiedz TYLKO RAZ, zwięźle i konkretnie
- Bazuj wyłącznie na kontekście z bazy wiedzy
- Jeśli pytanie odnosi się do wcześniejszej rozmowy, uwzględnij historię
- NIE powtarzaj pytania ani nie generuj kolejnych pytań
- Zakończ odpowiedź gdy udzielisz pełnej informacji

Odpowiedź:"""

    # Call LLM using the initialized model
    return llm_model(prompt)
