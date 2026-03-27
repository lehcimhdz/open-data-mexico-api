from unittest.mock import AsyncMock, patch

import httpx

from open_data_mexico import DatosGobMX
from open_data_mexico._scrapers.datasets import (
    _get_total_pages,
    _parse_datasets_page,
    fetch_category_datasets,
)
from open_data_mexico.models import Category, Dataset
from server.app import app

# ---------------------------------------------------------------------------
# Unit tests for scraper helpers
# ---------------------------------------------------------------------------


def test_parse_datasets_page_extracts_fields(datasets_page_1_html):
    datasets = _parse_datasets_page(datasets_page_1_html)
    assert len(datasets) == 2

    first = datasets[0]
    assert first.slug == "incidencia_delictiva"
    assert first.title == "Incidencia delictiva"
    assert first.last_updated == "3 de marzo 2026"
    assert first.category_slug == "seguridad"
    assert first.organization_slug == "sesnsp"
    assert first.resource_count == 3
    assert "/dataset/incidencia_delictiva" in first.url


def test_parse_datasets_page_description_excludes_link(datasets_page_1_html):
    datasets = _parse_datasets_page(datasets_page_1_html)
    first = datasets[0]
    assert first.description is not None
    assert "Ver base de datos" not in first.description


def test_get_total_pages_returns_2(datasets_page_1_html):
    total = _get_total_pages(datasets_page_1_html)
    assert total == 2


def test_get_total_pages_single():
    single_page_html = """
    <html><body>
    <ul class="pagination">
      <li class="page-item active"><a class="page-link" href="/group/seguridad?page=1">1</a></li>
    </ul>
    </body></html>
    """
    total = _get_total_pages(single_page_html)
    assert total == 1


async def test_fetch_category_datasets_combines_pages(
    httpx_mock, datasets_page_1_html, datasets_page_2_html
):
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/group/seguridad", text=datasets_page_1_html
    )
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/group/seguridad?page=2", text=datasets_page_2_html
    )
    async with httpx.AsyncClient() as client:
        datasets = await fetch_category_datasets(client, "seguridad")
    assert len(datasets) == 3


# ---------------------------------------------------------------------------
# Client tests
# ---------------------------------------------------------------------------

MOCK_DATASETS = [
    Dataset(
        slug="incidencia_delictiva",
        title="Incidencia delictiva",
        last_updated="3 de marzo 2026",
        category_slug="seguridad",
        category_name="Seguridad",
        organization_slug="sesnsp",
        organization_name="SESNSP",
        resource_count=3,
        url="https://www.datos.gob.mx/dataset/incidencia_delictiva",
    ),
    Dataset(
        slug="bajas_personal",
        title="Bajas de personal",
        last_updated="12 de febrero 2026",
        category_slug="seguridad",
        category_name="Seguridad",
        organization_slug="secretaria_marina",
        organization_name="Secretaría de Marina (SEMAR)",
        resource_count=2,
        url="https://www.datos.gob.mx/dataset/bajas_personal",
    ),
]

MOCK_CATEGORY = Category(
    slug="seguridad",
    name="Seguridad",
    description="Datos sobre seguridad pública.",
    dataset_count=10,
    image_url="https://www.datos.gob.mx/uploads/group/seguridad.svg",
    url="https://www.datos.gob.mx/group/seguridad",
)


async def test_client_get_category_datasets():
    with patch(
        "open_data_mexico._scrapers.datasets.fetch_category_datasets",
        new=AsyncMock(return_value=MOCK_DATASETS),
    ):
        async with DatosGobMX() as client:
            result = await client.get_category_datasets("seguridad")
    assert len(result) == 2
    assert result[0].slug == "incidencia_delictiva"


# ---------------------------------------------------------------------------
# API endpoint tests
# ---------------------------------------------------------------------------


async def test_api_datasets_endpoint():
    with patch.object(DatosGobMX, "get_category", new=AsyncMock(return_value=MOCK_CATEGORY)):
        with patch.object(
            DatosGobMX, "get_category_datasets", new=AsyncMock(return_value=MOCK_DATASETS)
        ):
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.get("/categories/seguridad/datasets")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["category_slug"] == "seguridad"
    assert len(data["datasets"]) == 2


async def test_api_datasets_endpoint_category_not_found():
    with patch.object(DatosGobMX, "get_category", new=AsyncMock(return_value=None)):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/categories/nonexistent/datasets")

    assert response.status_code == 404
    assert "nonexistent" in response.json()["detail"]
