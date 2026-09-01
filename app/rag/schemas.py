"""Data schemas and metadata models for RAG pipeline."""

from typing import Literal, Optional
from pydantic import BaseModel, Field

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
    chunk_index: Optional[int] = Field(
        default=None, description="Zero-based index of the chunk within the document"
    )
    page: Optional[int] = Field(
        default=None, description="Page number for multi-page documents like PDF"
    )
