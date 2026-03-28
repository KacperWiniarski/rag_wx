# ingestion/ingest_to_es.py
from elasticsearch import helpers
from config.es_config import get_es, ES_INDEX

# Use centralized ES client configuration
client = get_es()

def ingest_document(text_chunks, embeddings):
    """
    Ingest documents with embeddings into Elasticsearch.
    """
    docs = []
    for i, (text, emb) in enumerate(zip(text_chunks, embeddings)):
        docs.append({
            "_op_type": "index",
            "_index": ES_INDEX,
            "_id": i,
            "text": text,
            "embedding": emb[0] if isinstance(emb, list) else emb  # jeśli embedding jest listą list
        })
    ingestion_timeout = 300
    response = helpers.bulk(client.options(request_timeout=ingestion_timeout), docs)
    return response
