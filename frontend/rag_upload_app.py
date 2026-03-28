import streamlit as st
import time
from ingestion.file_loader import load_file
from config.watsonx_config import get_embedding_model
from ingestion.ingest_to_es import ingest_document

def app():
    st.title("📄 Upload Documents to RAG")
    
    st.markdown("""
    Upload your documents to index them in the RAG system.
    
    **Supported formats:**
    - 📝 **TXT**: Plain text files
    - 📄 **PDF**: Both text-based and scanned PDFs (with OCR)
    
    **Note:** For scanned PDFs, make sure Tesseract OCR is installed on your system.
    """)

    uploaded_files = st.file_uploader(
        "Choose files to upload",
        accept_multiple_files=True,
        type=["txt", "pdf"],
        help="Upload TXT or PDF files. Multiple files can be selected."
    )

    if uploaded_files:
        all_chunks = []
        failed_files = []

        # --- Process each file ---
        st.subheader("📂 Processing Files")
        for uploaded_file in uploaded_files:
            with st.expander(f"📄 {uploaded_file.name}", expanded=True):
                try:
                    # Show file info
                    file_size = len(uploaded_file.getvalue()) / 1024  # KB
                    st.write(f"**Size:** {file_size:.2f} KB")
                    st.write(f"**Type:** {uploaded_file.type}")
                    
                    # Load and chunk file
                    with st.spinner(f"Processing {uploaded_file.name}..."):
                        chunks = load_file(uploaded_file)
                    
                    # Add metadata to chunks
                    chunks_with_metadata = [
                        {
                            "file": uploaded_file.name,
                            "text": chunk
                        }
                        for chunk in chunks
                    ]
                    
                    all_chunks.extend(chunks_with_metadata)
                    st.success(f"✅ Created {len(chunks)} chunks")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    failed_files.append(uploaded_file.name)
        
        # Show summary
        if failed_files:
            st.warning(f"⚠️ Failed to process {len(failed_files)} file(s): {', '.join(failed_files)}")
        
        if not all_chunks:
            st.error("❌ No chunks were created. Please check your files and try again.")
            st.stop()
        
        st.success(f"✅ Total: {len(all_chunks)} chunks from {len(uploaded_files) - len(failed_files)} file(s)")
        
        # --- Load embedding model ---
        st.subheader("🧠 Loading Embedding Model")
        try:
            with st.spinner("Loading embedding model..."):
                embed_model = get_embedding_model()
            
            if embed_model is None:
                st.error("❌ Failed to load embedding model!")
                st.stop()
            
            st.success("✅ Embedding model loaded")
        except Exception as e:
            st.error(f"❌ Error loading embedding model: {e}")
            st.stop()

        # --- Generate embeddings ---
        st.subheader("🔢 Generating Embeddings")
        embed_progress = st.progress(0, text="Generating embeddings...")
        
        embeddings = []
        failed_embeddings = 0
        
        for i, chunk in enumerate(all_chunks, start=1):
            try:
                vector = embed_model([chunk["text"]])[0]
                embeddings.append(vector)
            except Exception as e:
                st.warning(f"⚠️ Failed to create embedding for chunk {i}: {e}")
                failed_embeddings += 1
                # Add empty vector as placeholder
                embeddings.append(None)
            
            embed_progress.progress(i / len(all_chunks), text=f"Processing chunk {i}/{len(all_chunks)}")
        
        # Remove None embeddings
        valid_chunks = []
        valid_embeddings = []
        for chunk, emb in zip(all_chunks, embeddings):
            if emb is not None:
                valid_chunks.append(chunk)
                valid_embeddings.append(emb)
        
        if failed_embeddings > 0:
            st.warning(f"⚠️ Failed to create {failed_embeddings} embedding(s)")
        
        if not valid_embeddings:
            st.error("❌ No valid embeddings were created!")
            st.stop()
        
        st.success(f"✅ Created {len(valid_embeddings)} embeddings")

        # --- Ingest to Elasticsearch ---
        st.subheader("📤 Upload to Elasticsearch")
        
        if st.button("🚀 Ingest to Elasticsearch", type="primary"):
            ingest_progress = st.progress(0, text="Uploading to Elasticsearch...")
            
            try:
                # Simulate progress (actual upload happens in bulk)
                for p in range(1, 101):
                    ingest_progress.progress(p / 100, text=f"Uploading... {p}%")
                    time.sleep(0.01)
                
                # Actual ingestion
                response = ingest_document(valid_chunks, valid_embeddings)
                
                ingest_progress.empty()
                st.success("✅ Documents successfully ingested to RAG index!")
                
                # Show details
                with st.expander("📊 Ingestion Details"):
                    st.write(f"**Total chunks ingested:** {len(valid_chunks)}")
                    st.write(f"**Files processed:** {len(uploaded_files) - len(failed_files)}")
                    st.json(response)
                
            except Exception as e:
                ingest_progress.empty()
                st.error(f"❌ Ingestion failed: {str(e)}")
                st.info("💡 Check your Elasticsearch connection and credentials in .env file")
