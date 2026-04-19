from langchain_openai import ChatOpenAI
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODEL_NAME

def get_llm():
    """Returns a ChatOpenAI instance configured for OpenRouter."""
    return ChatOpenAI(
        model=MODEL_NAME,
        temperature=0.2,
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        default_headers={
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "NEURAL GRID v2"
        }
    )
