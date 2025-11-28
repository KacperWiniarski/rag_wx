from config.watsonx_config import get_embedding_model

def embed_texts(texts):
    model = get_embedding_model()
    return model.embed(texts)
