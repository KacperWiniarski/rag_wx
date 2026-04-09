import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def validate_env_variables():
    """
    Validate that all required environment variables are set.
    Exits the application with an error message if any are missing.
    """
    required_vars = {
        "WATSONX_API_KEY": "Watsonx.ai API key",
        "WATSONX_PROJECT_ID": "Watsonx.ai project ID",
        "ES_URL": "Elasticsearch URL",
        "ES_API_KEY": "Elasticsearch API key"
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"  - {var}: {description}")
    
    if missing_vars:
        print("❌ ERROR: Missing required environment variables:")
        print("\n".join(missing_vars))
        print("\n📝 Please create a .env file based on config/env.example")
        print("   and fill in all required values.")
        sys.exit(1)

# Validate environment variables on import
validate_env_variables()

# Elasticsearch configuration
ES_URL = os.getenv("ES_URL")
ES_API_KEY = os.getenv("ES_API_KEY")
ES_INDEX = os.getenv("ES_INDEX", "rag-documents")

# Watsonx.ai configuration
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_URL = os.getenv("WATSONX_URL", "https://eu-de.ml.cloud.ibm.com")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Watsonx model names
LLM_MODEL_ID = os.getenv("LLM_MODEL_ID", "meta-llama/llama-4-maverick-17b-128e-instruct-fp8")
EMBED_MODEL_ID = os.getenv("EMBED_MODEL_ID", "intfloat/multilingual-e5-large")
