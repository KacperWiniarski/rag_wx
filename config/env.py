import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Elasticsearch configuration
ES_URL = os.getenv("ES_URL")
ES_API_KEY = os.getenv("ES_API_KEY")
ES_INDEX = os.getenv("ES_INDEX", "rag-documents")

# Watsonx.ai configuration
WATSONX_APIKEY = os.getenv("WATSONX_APIKEY")
WATSONX_URL = os.getenv("WATSONX_URL", "https://eu-de.ml.cloud.ibm.com")

# Watsonx model names
LLM_MODEL_ID = os.getenv("LLM_MODEL_ID", "ibm/granite-20b-multilingual")
EMBED_MODEL_ID = os.getenv("EMBED_MODEL_ID", "ibm/slate-125m-english-rtrvr")
