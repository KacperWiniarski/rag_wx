import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Elasticsearch configuration
ES_URL = os.getenv("ES_URL")
ES_API_KEY = os.getenv("ES_API_KEY")
ES_INDEX = os.getenv("ES_INDEX", "rag-documents")

# Watsonx.ai configuration
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_URL = os.getenv("WATSONX_URL", "https://eu-de.ml.cloud.ibm.com")

# Watsonx model names
LLM_MODEL_ID = os.getenv("LLM_MODEL_ID", "meta-llama/llama-3-2-90b-vision-instruct")
EMBED_MODEL_ID = os.getenv("EMBED_MODEL_ID", "ibm/slate-125m-english-rtrvr")
