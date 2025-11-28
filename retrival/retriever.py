from config.es_config import get_es, ES_INDEX
from ingestion.embedding_generator import embed_texts

def search(query, k=3):
    es = get_es()
    query_vec = embed_texts([query])[0]

    response = es.search(
        index=ES_INDEX,
        knn={
            "field": "embedding",
            "query_vector": query_vec,
            "k": k,
            "num_candidates": 50
        }
    )
    return [hit["_source"]["content"] for hit in response["hits"]["hits"]]
