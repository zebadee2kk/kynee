"""Tests for FastAPI application."""

from fastapi.testclient import TestClient

from kynee_console_backend.app import create_app


def test_app_creation():
    """Test app creation."""
    app = create_app()
    assert app is not None


def test_health_check():
    """Test health check endpoint."""
    app = create_app()
    client = TestClient(app)

    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"
