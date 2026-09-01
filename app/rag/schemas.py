"""Data schemas and metadata models for RAG pipeline."""

from typing import Any, Dict, List, Literal, Optional
from langchain_core.documents import Document
from pydantic import BaseModel, ConfigDict, Field

SourceType = Literal["internal", "external"]


class DocumentMetadata(BaseModel):
    """Metadata schema for loaded documents and chunks."""

    source: str = Field(..., description="File path or URI of the document source")
    source_type: SourceType = Field(
        ..., description="Origin classification: 'internal' or 'external'"
    )
    file_name: str = Field(..., description="Name of the file including extension")
    file_extension: str = Field(
        ..., description="File extension with leading dot (e.g., .md, .txt, .pdf)"
    )
    title: Optional[str] = Field(
        default=None, description="Optional document title extracted or provided"
    )
    chunk_index: Optional[int] = Field(
        default=None, description="Zero-based index of the chunk within the document"
    )
    page: Optional[int] = Field(
        default=None, description="Page number for multi-page documents like PDF"
    )


class SearchResult(BaseModel):
    """Structured result returned by vector store and retriever."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    document: Document = Field(
        ..., description="Retrieved Document chunk with page_content and metadata"
    )
    score: float = Field(
        ..., description="Cosine similarity score (higher = more similar, typically 0.0 to 1.0)"
    )
    rank: int = Field(..., ge=1, description="1-based position in ranked search results")


class SerializedDocument(BaseModel):
    """Schema for individual document chunks persisted in JSON."""

    page_content: str = Field(..., description="Text content of the chunk")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Metadata dictionary"
    )


class IndexManifest(BaseModel):
    """Schema for safe, non-pickle metadata and documents persisted to disk."""

    version: str = Field(default="1.0", description="Index schema version")
    fingerprint: str = Field(
        ..., description="SHA-256 fingerprint of the indexed corpus and parameters"
    )
    embedding_model: str = Field(..., description="Name of the embedding model used")
    embedding_dimension: int = Field(
        ..., description="Dimension of embedding vectors"
    )
    chunk_size: int = Field(..., description="Chunk size setting at index time")
    chunk_overlap: int = Field(..., description="Chunk overlap setting at index time")
    total_documents: int = Field(
        ..., description="Total number of chunks stored in index"
    )
    created_at: str = Field(
        ..., description="ISO 8601 UTC timestamp of index creation"
    )
    documents: List[SerializedDocument] = Field(
        default_factory=list,
        description="List of serialized documents aligned with FAISS vector indices",
    )
