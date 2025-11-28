import streamlit as st
import time
from ingestion.file_loader import load_file
from config.watsonx_config import get_embedding_model
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

        # Ładowanie modelu embeddingów
        embed_model = get_embedding_model()
        if embed_model is None:
            st.error("Brak modelu embeddingów!")
            st.stop()
        st.success("Embedding model loaded ✅")

        # --- Progress bar dla embeddingów ---
        st.info("Generating embeddings...")
        embed_progress_placeholder = st.empty()
        embed_progress = embed_progress_placeholder.progress(0)

        embeddings = []
        for i, chunk in enumerate(chunks, start=1):
            try:
                vector = embed_model([chunk])[0]
                embeddings.append(vector)
            except Exception as e:
                st.error(f"Error creating embedding for chunk {i}: {e}")

            embed_progress.progress(i / len(chunks))
            time.sleep(0.02)

        st.success("Embeddings created ✅")

        # --- Sekcja ingest ---
        if st.button("Ingest to Elasticsearch"):
            st.info("Uploading chunks...")

            # Nowy, oddzielny loading bar
            ingest_progress_placeholder = st.empty()
            ingest_progress = ingest_progress_placeholder.progress(0)

            try:
                # Udawany progres po stronie aplikacji
                for p in range(1, 101):
                    ingest_progress.progress(p / 100)
                    time.sleep(0.01)

                # prawdziwy ingest
                response = ingest_document(chunks, embeddings)

                ingest_progress_placeholder.empty()
                st.success("Document ingested to RAG index ✅")
                st.write("Elasticsearch response:", response)

            except Exception as e:
                ingest_progress_placeholder.empty()
                st.error(f"Ingest error: {e}")
