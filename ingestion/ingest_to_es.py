# ingestion/ingest_to_es.py
from elasticsearch import Elasticsearch, helpers

ES_URL = "https://my-elasticsearch-project-d02264.es.eu-central-1.aws.elastic.cloud:443"
ES_API_KEY = "ZnlJenlwb0I2WjJRYmstdnlzVkc6eFZsMjFod2dFVUxXYnpEWGs1RVNhZw=="
ES_INDEX = "rag-documents"

client = Elasticsearch(
    ES_URL,
    api_key=ES_API_KEY,
)

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
