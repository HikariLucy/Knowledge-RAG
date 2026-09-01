"""Main entrypoint for KnowledgeFlow RAG FastAPI service."""

from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Asistente para consulta y recuperación de conocimiento organizacional.",
    version="0.1.0",
)

# Register API routes
app.include_router(api_router)


@app.get("/health", tags=["Health"])
async def health_check():
    """Service healthcheck endpoint."""
    return {
        "status": "ok",
        "service": settings.app_name,
    }
