from config.watsonx_config import get_embed_texts

embed_model = get_embed_texts()

def embed_texts(texts):
    return embed_model(texts)

