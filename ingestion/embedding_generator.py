from config.watsonx_config import get_embedding_model

embed_model = get_embedding_model()

def embed_texts(texts):
    return embed_model(texts)

