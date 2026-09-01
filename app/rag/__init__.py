"""RAG module for document loading, preprocessing, chunking, embeddings, and vector retrieval."""

from app.rag.chunking import split_documents, validate_chunking_parameters
from app.rag.embeddings import (
    BaseEmbeddings,
    DeterministicFakeEmbeddings,
    GeminiEmbeddings,
    get_document_title,
    prepare_document_for_embedding,
    prepare_query_for_embedding,
)
from app.rag.loaders import (
    infer_source_type,
    load_directory,
    load_document,
    load_knowledge_base,
)
from app.rag.retriever import Retriever
from app.rag.schemas import (
    DocumentMetadata,
    IndexManifest,
    SearchResult,
    SerializedDocument,
    SourceType,
)
from app.rag.vectorstore import (
    VectorStore,
    compute_index_fingerprint,
    validate_index_fingerprint,
)

__all__ = [
    "load_document",
    "load_directory",
    "load_knowledge_base",
    "infer_source_type",
    "split_documents",
    "validate_chunking_parameters",
    "DocumentMetadata",
    "SourceType",
    "SearchResult",
    "SerializedDocument",
    "IndexManifest",
    "BaseEmbeddings",
    "GeminiEmbeddings",
    "DeterministicFakeEmbeddings",
    "get_document_title",
    "prepare_document_for_embedding",
    "prepare_query_for_embedding",
    "VectorStore",
    "compute_index_fingerprint",
    "validate_index_fingerprint",
    "Retriever",
]
