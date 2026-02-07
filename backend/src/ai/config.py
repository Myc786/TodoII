"""AI agent configuration for OpenAI or Cohere API."""
import os
from openai import OpenAI


def get_openai_client() -> OpenAI:
    """
    Create OpenAI client.

    Supports two modes:
    1. OpenAI API (default): Set OPENAI_API_KEY
    2. Cohere API: Set COHERE_API_KEY and OPENAI_COMPAT_BASE_URL

    Returns:
        Configured OpenAI client
    """
    # Check for OpenAI API key first
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        return OpenAI(api_key=openai_key)

    # Fall back to Cohere via compatibility API
    cohere_key = os.getenv("COHERE_API_KEY")
    if cohere_key:
        base_url = os.getenv("OPENAI_COMPAT_BASE_URL", "https://api.cohere.ai/compatibility/v1")
        return OpenAI(base_url=base_url, api_key=cohere_key)

    # No API key configured
    raise ValueError("No AI API key configured. Set OPENAI_API_KEY or COHERE_API_KEY.")


def get_model_name() -> str:
    """
    Get configured model name.

    Returns:
        Model name based on which API is configured
    """
    # If using OpenAI, use gpt-4o-mini (cost effective)
    if os.getenv("OPENAI_API_KEY"):
        return os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")

    # If using Cohere
    return os.getenv("COHERE_MODEL_NAME", "command-r-plus-08-2024")
