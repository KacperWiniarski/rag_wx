from config.es_config import get_es, ES_INDEX, ES_MAPPING
from ingestion.file_loader import load_file
from ingestion.text_splitter import split_text
from ingestion.embedding_generator import embed_texts

def ingest_document(path):
    es = get_es()

    if not es.indices.exists(index=ES_INDEX):
        es.indices.create(index=ES_INDEX, body=ES_MAPPING)

    text = load_file(path)
    chunks = split_text(text)

    embeddings = embed_texts(chunks)

    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        doc = {
            "content": chunk,
            "embedding": emb,
            "source": path,
            "chunk_id": f"{path}-{i}",
        }
        es.index(index=ES_INDEX, document=doc)

    return len(chunks)
