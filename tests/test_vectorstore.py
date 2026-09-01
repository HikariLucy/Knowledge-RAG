"""Offline unit tests for FAISS VectorStore, cosine similarity search, filtering, and persistence."""

import json
from pathlib import Path
import pytest
from langchain_core.documents import Document

from app.core.config import Settings
from app.rag.embeddings import DeterministicFakeEmbeddings
from app.rag.vectorstore import (
    VectorStore,
    compute_index_fingerprint,
    validate_index_fingerprint,
)


@pytest.fixture
def sample_documents():
    """Fixture providing mixed internal and external document chunks."""
    return [
        Document(
            page_content="Protocolo de respuesta ante incidentes de seguridad de la información.",
            metadata={
                "source": "knowledge/internal/seguridad.md",
                "source_type": "internal",
                "file_name": "seguridad.md",
                "chunk_index": 0,
            },
        ),
        Document(
            page_content="Procedimiento de autenticación multifactor para acceso remoto.",
            metadata={
                "source": "knowledge/internal/seguridad.md",
                "source_type": "internal",
                "file_name": "seguridad.md",
                "chunk_index": 1,
            },
        ),
        Document(
            page_content="Guía OWASP Top 10 de vulnerabilidades en aplicaciones web.",
            metadata={
                "source": "knowledge/external/owasp.md",
                "source_type": "external",
                "file_name": "owasp.md",
                "chunk_index": 0,
            },
        ),
        Document(
            page_content="Estándares NIST para gestión de contraseñas y criptografía.",
            metadata={
                "source": "knowledge/external/nist.txt",
                "source_type": "external",
                "file_name": "nist.txt",
                "chunk_index": 0,
            },
        ),
    ]


@pytest.fixture
def fake_embeddings_provider():
    """Fixture providing a deterministic fake embeddings provider."""
    return DeterministicFakeEmbeddings(embedding_dimension=768)


def test_vectorstore_stores_n_vectors(sample_documents, fake_embeddings_provider):
    """Verify FAISS vector store holds exactly N vectors corresponding to N documents."""
    embeddings = fake_embeddings_provider.embed_documents(sample_documents)
    vs = VectorStore.from_documents(sample_documents, embeddings)

    assert vs.index.ntotal == len(sample_documents)
    assert len(vs.documents) == len(sample_documents)
    assert vs.dimension == 768


def test_vectorstore_empty_documents():
    """Verify vectorstore handles empty document list gracefully."""
    vs = VectorStore.from_documents([], [])
    assert vs.index.ntotal == 0
    assert len(vs.documents) == 0

    query_vec = [0.1] * 768
    results = vs.similarity_search(query_vec, k=4)
    assert results == []


def test_vectorstore_search_results_sorted_descending(
    sample_documents, fake_embeddings_provider
):
    """Verify similarity search returns results sorted in descending order of score."""
    embeddings = fake_embeddings_provider.embed_documents(sample_documents)
    vs = VectorStore.from_documents(sample_documents, embeddings)

    query_vec = fake_embeddings_provider.embed_query("seguridad incidentes")
    results = vs.similarity_search(query_vec, k=4)

    assert len(results) <= 4
    for i in range(len(results) - 1):
        assert results[i].score >= results[i + 1].score
        assert results[i].rank == i + 1


def test_vectorstore_metadata_preserved(
    sample_documents, fake_embeddings_provider
):
    """Verify chunk metadata is completely preserved in search results."""
    embeddings = fake_embeddings_provider.embed_documents(sample_documents)
    vs = VectorStore.from_documents(sample_documents, embeddings)

    query_vec = fake_embeddings_provider.embed_query("OWASP vulnerabilidades")
    results = vs.similarity_search(query_vec, k=1)

    assert len(results) == 1
    doc = results[0].document
    assert "source" in doc.metadata
    assert "source_type" in doc.metadata
    assert "file_name" in doc.metadata


def test_vectorstore_filter_internal(
    sample_documents, fake_embeddings_provider
):
    """Verify filtering by internal sources returns only internal documents."""
    embeddings = fake_embeddings_provider.embed_documents(sample_documents)
    vs = VectorStore.from_documents(sample_documents, embeddings)

    query_vec = fake_embeddings_provider.embed_query("seguridad")
    results = vs.similarity_search(query_vec, k=4, source_type="internal")

    assert len(results) == 2
    for r in results:
        assert r.document.metadata["source_type"] == "internal"


def test_vectorstore_filter_external(
    sample_documents, fake_embeddings_provider
):
    """Verify filtering by external sources returns only external documents."""
    embeddings = fake_embeddings_provider.embed_documents(sample_documents)
    vs = VectorStore.from_documents(sample_documents, embeddings)

    query_vec = fake_embeddings_provider.embed_query("seguridad")
    results = vs.similarity_search(query_vec, k=4, source_type="external")

    assert len(results) == 2
    for r in results:
        assert r.document.metadata["source_type"] == "external"


def test_vectorstore_exact_top_k_with_filter(fake_embeddings_provider):
    """Verify that filtering returns exact Top-K items from the filtered subset even if other sources have higher global scores."""
    # 5 external docs, 2 internal docs
    docs = [
        Document(
            page_content=f"External doc {i}",
            metadata={"source_type": "external", "source": f"ext_{i}.txt", "file_name": f"ext_{i}.txt"},
        )
        for i in range(5)
    ] + [
        Document(
            page_content=f"Internal doc {i}",
            metadata={"source_type": "internal", "source": f"int_{i}.txt", "file_name": f"int_{i}.txt"},
        )
        for i in range(2)
    ]

    embeddings = fake_embeddings_provider.embed_documents(docs)
    vs = VectorStore.from_documents(docs, embeddings)

    query_vec = fake_embeddings_provider.embed_query("doc")
    # Request k=2 for internal: must return exactly 2 internal docs
    internal_results = vs.similarity_search(query_vec, k=2, source_type="internal")
    assert len(internal_results) == 2
    for r in internal_results:
        assert r.document.metadata["source_type"] == "internal"

    # Request k=3 for external: must return exactly 3 external docs
    external_results = vs.similarity_search(query_vec, k=3, source_type="external")
    assert len(external_results) == 3
    for r in external_results:
        assert r.document.metadata["source_type"] == "external"


def test_vectorstore_invalid_k_raises(sample_documents, fake_embeddings_provider):
    """Verify k <= 0 raises ValueError."""
    embeddings = fake_embeddings_provider.embed_documents(sample_documents)
    vs = VectorStore.from_documents(sample_documents, embeddings)
    query_vec = fake_embeddings_provider.embed_query("test")

    with pytest.raises(ValueError, match="positive"):
        vs.similarity_search(query_vec, k=0)

    with pytest.raises(ValueError, match="positive"):
        vs.similarity_search(query_vec, k=-3)


def test_vectorstore_invalid_source_type_raises(
    sample_documents, fake_embeddings_provider
):
    """Verify invalid source_type raises ValueError."""
    embeddings = fake_embeddings_provider.embed_documents(sample_documents)
    vs = VectorStore.from_documents(sample_documents, embeddings)
    query_vec = fake_embeddings_provider.embed_query("test")

    with pytest.raises(ValueError, match="Invalid source_type"):
        vs.similarity_search(query_vec, k=2, source_type="confidential")  # type: ignore


def test_save_and_load_local_preserves_results(
    sample_documents, fake_embeddings_provider, tmp_path
):
    """Verify save_local and load_local preserves index, documents, and search accuracy without pickle."""
    embeddings = fake_embeddings_provider.embed_documents(sample_documents)
    vs = VectorStore.from_documents(sample_documents, embeddings)

    # Save to tmp directory
    save_dir = tmp_path / "test_vectorstore"
    vs.save_local(save_dir)

    # Verify files created on disk
    assert (save_dir / "index.faiss").exists()
    assert (save_dir / "documents.json").exists()
    assert not any(save_dir.glob("*.pkl"))

    # Verify JSON content is safe and valid
    with open(save_dir / "documents.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["total_documents"] == len(sample_documents)
        assert data["embedding_dimension"] == 768
        assert "fingerprint" in data

    # Load from disk
    loaded_vs = VectorStore.load_local(save_dir)
    assert loaded_vs.index.ntotal == len(sample_documents)
    assert len(loaded_vs.documents) == len(sample_documents)

    # Verify search parity between in-memory and loaded vectorstore
    query_vec = fake_embeddings_provider.embed_query("incidente seguridad")
    res_orig = vs.similarity_search(query_vec, k=3)
    res_loaded = loaded_vs.similarity_search(query_vec, k=3)

    assert len(res_orig) == len(res_loaded)
    for r1, r2 in zip(res_orig, res_loaded):
        assert r1.score == pytest.approx(r2.score, rel=1e-5)
        assert r1.document.page_content == r2.document.page_content
        assert r1.document.metadata == r2.document.metadata


def test_fingerprint_deterministic_and_independent_of_vectors(
    sample_documents,
):
    """Verify index fingerprint is deterministic and strictly calculated from documents and parameters."""
    settings = Settings(
        chunk_size=500,
        chunk_overlap=50,
        embedding_dimension=768,
        gemini_embedding_model="gemini-embedding-2",
    )

    fp1 = compute_index_fingerprint(sample_documents, settings)
    fp2 = compute_index_fingerprint(sample_documents, settings)
    assert fp1 == fp2
    assert len(fp1) == 64  # SHA-256 hex length


def test_fingerprint_detects_document_modification(sample_documents):
    """Verify fingerprint changes when document content or metadata changes."""
    settings = Settings()
    original_fp = compute_index_fingerprint(sample_documents, settings)

    modified_docs = [
        Document(
            page_content="Contenido modificado",
            metadata=sample_documents[0].metadata.copy(),
        )
    ] + sample_documents[1:]

    modified_fp = compute_index_fingerprint(modified_docs, settings)
    assert original_fp != modified_fp


def test_fingerprint_detects_config_modification(sample_documents):
    """Verify fingerprint changes when chunk size or embedding dimension changes."""
    settings_a = Settings(chunk_size=500, embedding_dimension=768)
    settings_b = Settings(chunk_size=1000, embedding_dimension=768)
    settings_c = Settings(chunk_size=500, embedding_dimension=1536)

    fp_a = compute_index_fingerprint(sample_documents, settings_a)
    fp_b = compute_index_fingerprint(sample_documents, settings_b)
    fp_c = compute_index_fingerprint(sample_documents, settings_c)

    assert fp_a != fp_b
    assert fp_a != fp_c


def test_validate_index_fingerprint(sample_documents, fake_embeddings_provider):
    """Verify validate_index_fingerprint returns True for matched and False for stale index."""
    settings = Settings()
    embeddings = fake_embeddings_provider.embed_documents(sample_documents)
    vs = VectorStore.from_documents(sample_documents, embeddings, settings=settings)

    assert validate_index_fingerprint(vs.manifest, sample_documents, settings) is True

    # Alter documents
    stale_docs = sample_documents[:-1]
    assert validate_index_fingerprint(vs.manifest, stale_docs, settings) is False
