"""AI agent configuration for Cohere via OpenAI compatibility API."""
import os
from openai import OpenAI


def get_openai_client() -> OpenAI:
    """
    Create OpenAI client configured for Cohere via compatibility API.

    Uses environment variables:
    - COHERE_API_KEY: Cohere API key
    - OPENAI_COMPAT_BASE_URL: Cohere OpenAI-compatible endpoint
    - COHERE_MODEL_NAME: Cohere model name (default: command-r-plus)

    Returns:
        OpenAI client configured for Cohere
    """
    return OpenAI(
        base_url=os.getenv("OPENAI_COMPAT_BASE_URL", "https://api.cohere.ai/v1"),
        api_key=os.getenv("COHERE_API_KEY")
    )


def get_model_name() -> str:
    """
    Get configured Cohere model name.

    Returns:
        Model name from environment or default
    """
    return os.getenv("COHERE_MODEL_NAME", "command-r-plus")
