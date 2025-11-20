from typing import List
from openai import OpenAI

from .config import config

_client: OpenAI | None = None


def get_client() -> OpenAI:
    """
    Lazily initialize a global OpenAI client.
    Relies on OPENAI_API_KEY being set in the environment.
    """
    global _client
    if _client is None:
        if not config.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not set in the environment.")
        # New OpenAI client style
        _client = OpenAI(api_key=config.openai_api_key)
    return _client


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Given a list of strings, return a list of embedding vectors.
    """
    client = get_client()
    response = client.embeddings.create(
        model=config.embedding_model,
        input=texts,
    )
    return [item.embedding for item in response.data]
