from config.watsonx_config import get_llm_model
from retrieval.retriever import search


llm_model = get_llm_model()


def rag_answer(question):
    # pobierz kontekst z retrievera
    context_chunks = search(question)
    context = "\n".join(context_chunks)

    # przygotuj prompt
    prompt = f"""
You are a RAG assistant.
Context:
{context}

Question: {question}
Answer factually based only on context.
"""

    # wywołanie LLM
    return get_llm_model(prompt)  # <-- teraz po prostu wywołujemy funkcję
