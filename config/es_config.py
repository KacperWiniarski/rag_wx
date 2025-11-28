from elasticsearch import Elasticsearch
from config.env import ES_URL, ES_API_KEY, ES_INDEX

def get_es():
    return Elasticsearch(
        ES_URL,
        api_key=ES_API_KEY
    )

ES_MAPPING = {
    "mappings": {
        "properties": {
            "content": {"type": "text"},
            "embedding": {
                "type": "dense_vector",
                "dims": 384,
                "index": True,
                "similarity": "cosine"
            },
            "source": {"type": "keyword"},
            "chunk_id": {"type": "keyword"}
        }
    }
}
