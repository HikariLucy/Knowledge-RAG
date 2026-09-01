"""Centralized application configuration using Pydantic Settings."""

from functools import lru_cache
from typing import Optional
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings and environment variables."""

    # Application Info
    app_name: str = "KnowledgeFlow RAG"
    app_env: str = "development"

    # LLM Provider (Google Gemini)
    gemini_api_key: Optional[str] = None
    gemini_chat_model: str = "gemini-3.5-flash"
    gemini_embedding_model: str = "gemini-embedding-2"

    # Document Chunking Defaults
    chunk_size: int = 500
    chunk_overlap: int = 50

    # Vector Store & Retrieval Defaults
    embedding_dimension: int = 768
    retrieval_top_k: int = 4
    vectorstore_dir: str = "vectorstore"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @model_validator(mode="after")
    def validate_parameters(self) -> "Settings":
        """Validate chunk and retrieval configuration parameters."""
        if self.chunk_size <= 0:
            raise ValueError(f"chunk_size must be positive, got {self.chunk_size}")
        if self.chunk_overlap < 0:
            raise ValueError(
                f"chunk_overlap must be non-negative, got {self.chunk_overlap}"
            )
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                f"chunk_overlap ({self.chunk_overlap}) must be strictly less than chunk_size ({self.chunk_size})"
            )
        if self.embedding_dimension <= 0:
            raise ValueError(
                f"embedding_dimension must be positive, got {self.embedding_dimension}"
            )
        if self.retrieval_top_k <= 0:
            raise ValueError(
                f"retrieval_top_k must be positive, got {self.retrieval_top_k}"
            )
        return self


@lru_cache()
def get_settings() -> Settings:
    """Retrieve cached application settings instance."""
    return Settings()
