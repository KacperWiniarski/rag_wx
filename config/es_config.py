from elasticsearch import Elasticsearch
from config.env import ES_URL, ES_API_KEY, ES_INDEX

def get_es():
    """
    Create and return an Elasticsearch client instance.
    
    Returns:
        Elasticsearch: Configured Elasticsearch client
    """
    return Elasticsearch(
        ES_URL,
        api_key=ES_API_KEY
    )

# Elasticsearch index mapping
# Note: dims=1024 for intfloat/multilingual-e5-large model
# If using a different embedding model, adjust dims accordingly:
# - intfloat/multilingual-e5-large: 1024
# - ibm/slate-125m-english-rtrvr: 768
# - sentence-transformers/all-MiniLM-L6-v2: 384
ES_MAPPING = {
    "mappings": {
        "properties": {
            "content": {"type": "text"},
            "embedding": {
                "type": "dense_vector",
                "dims": 1024,  # Updated for intfloat/multilingual-e5-large
                "index": True,
                "similarity": "cosine"
            },
            "source": {"type": "keyword"},
            "chunk_id": {"type": "keyword"}
        }
    }
}
