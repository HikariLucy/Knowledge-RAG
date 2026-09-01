"""CLI demonstration tool for semantic search and retrieval without LLM generation."""

import argparse
import sys
from typing import Optional

from app.core.config import Settings, get_settings
from app.rag.embeddings import BaseEmbeddings, GeminiEmbeddings
from app.rag.retriever import Retriever
from app.rag.schemas import SourceType
from app.rag.vectorstore import VectorStore


def run_search(
    query: str,
    k: int = 4,
    source_type: Optional[SourceType] = None,
    vectorstore_dir: Optional[str] = None,
    embeddings_provider: Optional[BaseEmbeddings] = None,
    settings: Optional[Settings] = None,
) -> None:
    """Execute search query against persisted vector store and print formatted results.

    Args:
        query: Search query string.
        k: Number of Top-K results.
        source_type: Optional filter ('internal' or 'external').
        vectorstore_dir: Path to directory containing saved index.
        embeddings_provider: Custom embeddings provider (defaults to GeminiEmbeddings).
        settings: Application settings.
    """
    cfg = settings or get_settings()
    vdir = vectorstore_dir or cfg.vectorstore_dir

    try:
        vectorstore = VectorStore.load_local(vdir)
    except FileNotFoundError as e:
        print(
            f"Error: Vector store not found in '{vdir}'. Run 'python -m app.rag.indexer' first.\n({e})",
            file=sys.stderr,
        )
        sys.exit(1)

    provider = embeddings_provider or GeminiEmbeddings(settings=cfg)
    retriever = Retriever(
        vectorstore=vectorstore, embeddings=provider, settings=cfg
    )

    results = retriever.search(query=query, k=k, source_type=source_type)

    print("========================================")
    print("      KnowledgeFlow RAG Search Demo     ")
    print("========================================")
    print(f"Query:       {query}")
    print(f"Top-K:       {k}")
    print(f"Filter:      {source_type or 'None (All Sources)'}")
    print(f"Results:     {len(results)} found")
    print("========================================\n")

    if not results:
        print("No matching documents found.")
        return

    for res in results:
        meta = res.document.metadata or {}
        snippet = res.document.page_content.strip()
        if len(snippet) > 300:
            snippet = snippet[:300] + "..."

        print(f"[{res.rank}] Score (Cosine Sim): {res.score:.4f}")
        print(f"    Source Type: {meta.get('source_type', 'N/A')}")
        print(f"    Source:      {meta.get('source', 'N/A')}")
        print(f"    File:        {meta.get('file_name', 'N/A')}")
        print(f"    Chunk Index: {meta.get('chunk_index', 'N/A')}")
        if meta.get("page") is not None:
            print(f"    Page:        {meta.get('page')}")
        print(f"    Text Preview:\n      {snippet}\n")


def main() -> None:
    """CLI argument parser and runner."""
    parser = argparse.ArgumentParser(
        description="Search KnowledgeFlow FAISS Vector Store"
    )
    parser.add_argument(
        "query",
        type=str,
        help="Search query text",
    )
    parser.add_argument(
        "-k",
        "--top-k",
        type=int,
        default=4,
        help="Number of results to retrieve (default: 4)",
    )
    parser.add_argument(
        "-s",
        "--source-type",
        type=str,
        choices=["internal", "external"],
        default=None,
        help="Filter source type: 'internal' or 'external'",
    )
    parser.add_argument(
        "-v",
        "--vectorstore-dir",
        type=str,
        default=None,
        help="Custom vector store directory (default: from config)",
    )

    args = parser.parse_args()

    try:
        run_search(
            query=args.query,
            k=args.top_k,
            source_type=args.source_type,
            vectorstore_dir=args.vectorstore_dir,
        )
    except Exception as e:
        print(f"Error during search: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
