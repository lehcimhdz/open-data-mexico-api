"""Tests for the FastAPI server's meta endpoints and middleware."""

import importlib

import httpx

from open_data_mexico import __version__
from server.app import app


async def test_health_endpoint():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body == {"status": "ok", "version": __version__}


async def test_root_endpoint_includes_version():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] == __version__


async def test_cors_header_present_on_preflight():
    """OPTIONS preflight should reflect the configured CORS allow-list."""
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.options(
            "/health",
            headers={
                "Origin": "https://example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
    assert response.status_code == 200
    assert "access-control-allow-origin" in {k.lower() for k in response.headers}


def test_allowed_origins_default_wildcard(monkeypatch):
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    import server.app as srv

    importlib.reload(srv)
    assert srv._allowed_origins() == ["*"]


def test_allowed_origins_csv(monkeypatch):
    monkeypatch.setenv("CORS_ORIGINS", "https://a.com, https://b.com")
    import server.app as srv

    importlib.reload(srv)
    assert srv._allowed_origins() == ["https://a.com", "https://b.com"]
    # Reset env so other tests see the default again
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    importlib.reload(srv)
