from config.watsonx_config import get_llm
from retrieval.retriever import search

def rag_answer(question):
    context_chunks = search(question)
    context = "\n".join(context_chunks)

    prompt = f"""
    You are a RAG assistant.
    Context:
    {context}

    Question: {question}
    Answer factually based only on context.
    """

    llm = get_llm()
    return llm.generate(prompt)
