from ibm_watsonx_ai import WatsonxLLM, WatsonxEmbeddings
from config.env import (
    WATSONX_APIKEY,
    WATSONX_URL,
    LLM_MODEL_ID,
    EMBED_MODEL_ID,
)

def get_llm():
    return WatsonxLLM(
        model_id=LLM_MODEL_ID,
        credentials={
            "apikey": WATSONX_APIKEY,
            "url": WATSONX_URL
        },
        params={"temperature": 0.1}
    )

def get_embedding_model():
    return WatsonxEmbeddings(
        model_id=EMBED_MODEL_ID,
        credentials={
            "apikey": WATSONX_APIKEY,
            "url": WATSONX_URL
        }
    )
