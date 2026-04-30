import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from dotenv import load_dotenv
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames as EmbedParams
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Embeddings

# Wczytaj .env (musisz mieć plik .env w tym samym katalogu co app.py)
load_dotenv()  
# --- Load credentials from ENV ---
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_URL = os.getenv("WATSONX_URL")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

LLM_MODEL_ID = os.getenv("LLM_MODEL_ID")
EMBED_MODEL_ID = os.getenv("EMBED_MODEL_ID")


def get_embedding_model():

    embed_params = {
        EmbedParams.TRUNCATE_INPUT_TOKENS: 512,
        EmbedParams.RETURN_OPTIONS: {"input_text": False}
    }

    embedding_model = Embeddings(
        model_id=EMBED_MODEL_ID,
        params=embed_params,
        credentials=Credentials(api_key=WATSONX_API_KEY, url=WATSONX_URL),
        project_id=WATSONX_PROJECT_ID
    )
    def embed_texts(text_list):
        results = []
        for text in text_list:
            # generate wymaga listy tekstów
            response = embedding_model.generate([text])
            vector = response["results"][0]["embedding"]
            results.append(vector)
        return results
    return embed_texts



def get_llm_model():
    """Zwraca LLM jako funkcję do wywołania promptu."""
    params = {
        GenParams.MAX_NEW_TOKENS: 600,
        GenParams.MIN_NEW_TOKENS: 20,
        GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
        GenParams.TEMPERATURE: 0.2,
        GenParams.REPETITION_PENALTY: 1.1,
        GenParams.STOP_SEQUENCES: ["\n\nUżytkownik:", "\n\nAktualne pytanie:", "Odpowiedz bazując"],
    }

    llm_model = ModelInference(
        model_id=LLM_MODEL_ID,
        params=params,
        credentials={"apikey": WATSONX_API_KEY, "url": WATSONX_URL},
        project_id=WATSONX_PROJECT_ID,
    )

    def generate_text(prompt):
        resp = llm_model.generate(prompt=prompt)
        return resp["results"][0]["generated_text"]

    return generate_text
