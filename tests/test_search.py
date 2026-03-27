from unittest.mock import AsyncMock, patch

import httpx
import pytest

from open_data_mexico import DatosGobMX, SearchResponse
from open_data_mexico._scrapers.search import _parse_package, search_datasets
from server.app import app

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

CKAN_PACKAGE = {
    "name": "rezago_social",
    "title": "Rezago social",
    "notes": "Medida que permite ordenar unidades geográficas.",
    "metadata_modified": "2025-06-04T18:44:31.334457",
    "num_resources": 17,
    "groups": [{"name": "poblacion", "display_name": "Población"}],
    "organization": {
        "name": "coneval",
        "title": "Consejo Nacional de Evaluación de la Política de Desarrollo Social (CONEVAL)",
    },
}

CKAN_RESPONSE = {
    "success": True,
    "result": {
        "count": 2,
        "results": [CKAN_PACKAGE],
    },
}


# ---------------------------------------------------------------------------
# Unit tests — _parse_package
# ---------------------------------------------------------------------------


def test_parse_package_maps_fields():
    ds = _parse_package(CKAN_PACKAGE)
    assert ds.slug == "rezago_social"
    assert ds.title == "Rezago social"
    assert ds.last_updated == "2025-06-04T18:44:31.334457"
    assert ds.description == "Medida que permite ordenar unidades geográficas."
    assert ds.category_slug == "poblacion"
    assert ds.category_name == "Población"
    assert ds.organization_slug == "coneval"
    assert ds.organization_name is not None and "CONEVAL" in ds.organization_name
    assert ds.resource_count == 17
    assert ds.url == "https://www.datos.gob.mx/dataset/rezago_social"


def test_parse_package_empty_groups():
    pkg = {**CKAN_PACKAGE, "groups": []}
    ds = _parse_package(pkg)
    assert ds.category_slug is None
    assert ds.category_name is None


def test_parse_package_no_organization():
    pkg = {**CKAN_PACKAGE, "organization": None}
    ds = _parse_package(pkg)
    assert ds.organization_slug is None
    assert ds.organization_name is None


# ---------------------------------------------------------------------------
# Integration tests — search_datasets (httpx_mock)
# ---------------------------------------------------------------------------


async def test_search_datasets_returns_total_and_list(httpx_mock):
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/api/3/action/package_search?q=rezago+social&rows=20&start=0&sort=metadata_modified+desc",
        json=CKAN_RESPONSE,
    )
    async with httpx.AsyncClient() as client:
        total, datasets = await search_datasets(client, "rezago social")
    assert total == 2
    assert len(datasets) == 1
    assert datasets[0].slug == "rezago_social"


async def test_search_datasets_with_category_filter(httpx_mock):
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/api/3/action/package_search?q=salud&rows=5&start=0&sort=metadata_modified+desc&fq=groups%3Asalud",
        json={**CKAN_RESPONSE, "result": {**CKAN_RESPONSE["result"], "count": 10}},
    )
    async with httpx.AsyncClient() as client:
        total, datasets = await search_datasets(client, "salud", category="salud", limit=5)
    assert total == 10


async def test_search_datasets_raises_on_api_error(httpx_mock):
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/api/3/action/package_search?q=x&rows=20&start=0&sort=metadata_modified+desc",
        json={"success": False, "error": {"message": "bad request"}},
    )
    async with httpx.AsyncClient() as client:
        with pytest.raises(ValueError, match="CKAN API error"):
            await search_datasets(client, "x")


# ---------------------------------------------------------------------------
# Client integration — DatosGobMX.search()
# ---------------------------------------------------------------------------


async def test_client_search_returns_search_response():
    mock_result = (2, [_parse_package(CKAN_PACKAGE)])
    with patch(
        "open_data_mexico._scrapers.search.search_datasets",
        new=AsyncMock(return_value=mock_result),
    ):
        async with DatosGobMX() as client:
            resp = await client.search("rezago social")

    assert isinstance(resp, SearchResponse)
    assert resp.total == 2
    assert resp.query == "rezago social"
    assert resp.category is None
    assert resp.offset == 0
    assert len(resp.datasets) == 1


async def test_client_search_passes_category_and_pagination():
    mock_result = (5, [])
    with patch(
        "open_data_mexico._scrapers.search.search_datasets",
        new=AsyncMock(return_value=mock_result),
    ) as mock_fn:
        async with DatosGobMX() as client:
            resp = await client.search("agua", category="medio_ambiente", limit=5, offset=10)

    assert resp.category == "medio_ambiente"
    assert resp.offset == 10
    _, kwargs = mock_fn.call_args
    assert kwargs["category"] == "medio_ambiente"
    assert kwargs["limit"] == 5
    assert kwargs["offset"] == 10


# ---------------------------------------------------------------------------
# API endpoint — GET /search
# ---------------------------------------------------------------------------


async def test_api_search_endpoint():
    mock_resp = SearchResponse(
        total=2,
        query="rezago social",
        category=None,
        offset=0,
        datasets=[_parse_package(CKAN_PACKAGE)],
    )
    with patch.object(DatosGobMX, "search", new=AsyncMock(return_value=mock_resp)):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/search", params={"q": "rezago social"})

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["query"] == "rezago social"
    assert len(data["datasets"]) == 1
    assert data["datasets"][0]["slug"] == "rezago_social"


async def test_api_search_endpoint_with_category():
    mock_resp = SearchResponse(
        total=1, query="agua", category="medio_ambiente", offset=0, datasets=[]
    )
    with patch.object(DatosGobMX, "search", new=AsyncMock(return_value=mock_resp)):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get(
                "/search", params={"q": "agua", "category": "medio_ambiente"}
            )

    assert response.status_code == 200
    assert response.json()["category"] == "medio_ambiente"


async def test_api_search_missing_q_returns_422():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/search")
    assert response.status_code == 422
