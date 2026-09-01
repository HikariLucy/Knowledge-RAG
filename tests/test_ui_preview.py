"""Offline unit tests for UI Preview Server and fixture validation."""

import pytest
from fastapi.testclient import TestClient

from app.main import app as prod_app
from app.rag.schemas import QueryResponse
from scripts.ui_preview import app as preview_app, FIXTURES_PATH, PreviewRAGPipeline

preview_client = TestClient(preview_app)
prod_client = TestClient(prod_app)


def test_production_app_is_not_polluted_by_preview_import():
    """Verify that importing scripts.ui_preview does NOT pollute prod_app.dependency_overrides."""
    assert prod_app.dependency_overrides == {}


def test_preview_fixtures_file_exists_and_validates():
    """Verify preview fixture file exists and all scenarios match QueryResponse schema."""
    assert FIXTURES_PATH.exists()
    pipeline = PreviewRAGPipeline(FIXTURES_PATH)
    assert len(pipeline.fixtures) >= 5

    for scenario_name, scenario_data in pipeline.fixtures.items():
        # Validate that each fixture fits QueryResponse
        response_model = QueryResponse(**scenario_data)
        assert response_model.query is not None
        assert response_model.source_scope in ["internal", "external", "all"]


def test_preview_ui_root_serves_html():
    """Verify GET / on preview app returns 200 with UI HTML."""
    response = preview_client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "KnowledgeFlow" in response.text


def test_preview_health_endpoint():
    """Verify GET /health on preview app returns preview mode."""
    response = preview_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["mode"] == "preview_offline"


def test_preview_scenario_a_internal():
    """Verify preview returns internal scenario with S1 and S2."""
    response = preview_client.post(
        "/api/query",
        json={"query": "¿Qué requisitos deben cumplir las contraseñas internas?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["source_scope"] == "internal"
    assert data["abstained"] is False
    assert "S1" in data["citations"]
    assert len(data["sources"]) >= 2
    assert all(s["source_type"] == "internal" for s in data["sources"])


def test_preview_scenario_b_external():
    """Verify preview returns external scenario with OWASP sources."""
    response = preview_client.post(
        "/api/query",
        json={"query": "¿Cómo se previene Prompt Injection según OWASP?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["source_scope"] == "external"
    assert data["abstained"] is False
    assert "S1" in data["citations"]
    assert any("owasp" in s["file_name"] for s in data["sources"])


def test_preview_scenario_c_mixed():
    """Verify preview returns mixed scenario with both internal and external sources."""
    response = preview_client.post(
        "/api/query",
        json={"query": "Compara el procedimiento interno de incidentes con buenas prácticas externas."},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["source_scope"] == "all"
    assert data["abstained"] is False
    source_types = {s["source_type"] for s in data["sources"]}
    assert "internal" in source_types
    assert "external" in source_types


def test_preview_scenario_d_abstention():
    """Verify preview returns abstention state for out-of-domain query."""
    response = preview_client.post(
        "/api/query",
        json={"query": "¿Cuál es la velocidad de la luz en el vacío?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["abstained"] is True
    assert data["citations"] == []
    assert data["sources"] == []


def test_preview_scenario_e_density():
    """Verify preview returns 4 sources and 4 citations for density scenario."""
    response = preview_client.post(
        "/api/query",
        json={"query": "Auditoría completa y densidad de citas"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["abstained"] is False
    assert len(data["sources"]) == 4
    assert len(data["citations"]) == 4


def test_preview_error_500_trigger():
    """Verify PREVIEW_ERROR_500 trigger produces HTTP 500."""
    response = preview_client.post(
        "/api/query",
        json={"query": "PREVIEW_ERROR_500"},
    )
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data


def test_preview_error_503_trigger():
    """Verify PREVIEW_ERROR_503 trigger produces HTTP 503."""
    response = preview_client.post(
        "/api/query",
        json={"query": "PREVIEW_ERROR_503"},
    )
    assert response.status_code == 503
    data = response.json()
    assert "detail" in data
