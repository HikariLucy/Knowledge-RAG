"""Tests for configuration and decoupled LLM client."""

import pytest
from app.core.config import Settings
from app.llm.client import GeminiClient


def test_settings_defaults():
    """Verify default configuration settings."""
    settings = Settings(
        app_name="KnowledgeFlow RAG",
        chunk_size=500,
        chunk_overlap=50,
    )
    assert settings.app_name == "KnowledgeFlow RAG"
    assert settings.chunk_size == 500
    assert settings.chunk_overlap == 50
    assert settings.gemini_chat_model == "gemini-2.5-flash"
    assert settings.gemini_embedding_model == "text-embedding-004"


def test_gemini_client_unconfigured():
    """Verify GeminiClient behaves safely when API key is missing."""
    settings = Settings(gemini_api_key=None)
    client = GeminiClient(settings=settings)

    assert client.is_configured is False
    with pytest.raises(RuntimeError, match="GEMINI_API_KEY is not configured"):
        client.get_client()


def test_gemini_client_configured_property():
    """Verify is_configured returns True when key is set."""
    settings = Settings(gemini_api_key="demo-test-api-key")
    client = GeminiClient(settings=settings)

    assert client.is_configured is True
