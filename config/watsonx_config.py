import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import ModelInference

# Wczytaj .env (musisz mieć plik .env w tym samym katalogu co app.py)
load_dotenv()  
# --- Load credentials from ENV ---
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_URL = os.getenv("WATSONX_URL")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

LLM_MODEL_ID = os.getenv("LLM_MODEL_ID")
EMBED_MODEL_ID = os.getenv("EMBED_MODEL_ID")

# Inicjalizacja modelu (tylko id + credentials)
embed_model = ModelInference(
    model_id=EMBED_MODEL_ID,
    credentials={"apikey": WATSONX_API_KEY, "url": WATSONX_URL},
    project_id=WATSONX_PROJECT_ID
)

def get_embed_texts(texts):
    embeddings = []
    for text in texts:
        # embedding model w tym SDK wymaga generate() ale zwraca embeddingi
        resp = embed_model.generate(prompt=text)
        vector = resp["results"][0]["embedding"]  # tutaj mamy wektor
        embeddings.append(vector)
    return embeddings


def get_llm_model():
    """Zwraca LLM jako funkcję do wywołania promptu."""
    llm_model = ModelInference(
        model_id=LLM_MODEL_ID,
        credentials={"apikey": WATSONX_API_KEY, "url": WATSONX_URL},
        project_id=WATSONX_PROJECT_ID,
    )

    def generate_text(prompt):
        resp = llm_model.generate(prompt=prompt)
        return resp["results"][0]["text"]

    return generate_text
