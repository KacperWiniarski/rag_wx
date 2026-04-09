from config.watsonx_config import get_llm_model
from retrieval.retriever import search


llm_model = get_llm_model()


def rag_answer(question):
    """
    Generate an answer to a question using RAG (Retrieval-Augmented Generation).
    
    Args:
        question (str): The user's question
        
    Returns:
        str: The generated answer based on retrieved context
    """
    # Retrieve context from the retriever
    context_chunks = search(question)
    context = "\n".join(context_chunks)

    # Prepare prompt
    prompt = f"""
Jesteś asystentem AI wspierającym użytkowników. Odpowiadaj tylko po polsku i tylko na bazie konetekstu.
Kontekst:
{context}

Pytanie: {question}
Odpowiedz bazując jedynie na kontekście i pytaniu.
"""

    # Call LLM using the initialized model
    return llm_model(prompt)
