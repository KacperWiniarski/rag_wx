import streamlit as st
import os
from ingestion.ingest_to_es import ingest_document

st.title("📄 Upload documents to RAG")

uploaded = st.file_uploader("Upload file (PDF/TXT)", type=["pdf", "txt"])

if uploaded:
    path = os.path.join("data", uploaded.name)
    with open(path, "wb") as f:
        f.write(uploaded.getbuffer())

    chunks = ingest_document(path)
    st.success(f"Indexed {chunks} chunks!")
