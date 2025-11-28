import streamlit as st
import time
from ingestion.file_loader import load_file
from ingestion.embedding_generator import get_embed_texts # poprawiony import
from ingestion.ingest_to_es import ingest_document

def app():
    st.title("📄 Upload documents to RAG")

    uploaded_file = st.file_uploader("Choose a TXT file")

    if uploaded_file:
        raw_text = uploaded_file.read().decode("utf-8")

        # Chunkowanie
        try:
            chunks = load_file(uploaded_file)
            st.success(f"{len(chunks)} chunks created")
        except Exception as e:
            st.error(f"Chunking error: {e}")
            st.stop()

        st.success("Embedding setup loaded ✅")

        # Generowanie embeddingów
        embeddings = []
        st.info("Generating embeddings...")
        progress_bar = st.progress(0)

        for i, chunk in enumerate(chunks, start=1):
            try:
                # używamy funkcji embed_texts, która zwraca listę embeddingów
                vector = get_embed_texts([chunk])[0]
                embeddings.append(vector)
            except Exception as e:
                st.error(f"Error creating embedding for chunk {i}: {e}")

            if i % 5 == 0 or i == len(chunks):
                progress_bar.progress(i / len(chunks))
            time.sleep(0.05)

        st.success("Embeddings created ✅")

        # Ingest do Elasticsearch
        if st.button("Ingest to Elasticsearch"):
            st.info("Uploading chunks...")
            try:
                response = ingest_document(chunks, embeddings)
                st.success("Document ingested to RAG index ✅")
                st.write("Elasticsearch response:", response)
            except Exception as e:
                st.error(f"Ingest error: {e}")
