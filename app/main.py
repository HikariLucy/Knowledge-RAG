"""Main entrypoint for KnowledgeFlow RAG FastAPI service."""

from fastapi import FastAPI
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Asistente para consulta y recuperación de conocimiento organizacional.",
    version="0.1.0",
)


@app.get("/health", tags=["Health"])
async def health_check():
    """Service healthcheck endpoint."""
    return {
        "status": "ok",
        "service": settings.app_name,
    }
