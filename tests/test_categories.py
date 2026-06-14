from unittest.mock import AsyncMock, patch

import httpx

from open_data_mexico import DatosGobMX
from open_data_mexico._scrapers.categories import (
    _get_total_pages,
    _parse_categories_page,
    fetch_all_categories,
)
from open_data_mexico.models import Category
from server.app import app

# ---------------------------------------------------------------------------
# Unit tests for scraper helpers
# ---------------------------------------------------------------------------


async def test_parse_categories_page(categories_page_1_html):
    categories = await _parse_categories_page(categories_page_1_html)
    assert len(categories) == 2

    agri = categories[0]
    assert agri.slug == "agricultura"
    assert agri.name == "Agricultura"
    assert agri.description == "Datos sobre la actividad agrícola en México."
    assert agri.dataset_count == 139
    assert agri.image_url == "https://www.datos.gob.mx/uploads/group/agricultura.svg"
    assert agri.url == "https://www.datos.gob.mx/group/agricultura"

    edu = categories[1]
    assert edu.slug == "educacion"
    assert edu.name == "Educación"
    assert edu.dataset_count == 1204


async def test_get_total_pages_with_pagination(categories_page_1_html):
    total = await _get_total_pages(categories_page_1_html)
    assert total == 2


async def test_get_total_pages_single_page(categories_page_2_html):
    # Page 2 has no "next" (»), only pages 1 and 2 — but max is 2.
    # Create a minimal single-page HTML with only page 1 in pagination.
    single_page_html = """
    <html><body>
    <ul class="pagination">
      <li class="page-item active"><a class="page-link" href="/group/?page=1">1</a></li>
    </ul>
    </body></html>
    """
    total = await _get_total_pages(single_page_html)
    assert total == 1


async def test_fetch_all_categories_combines_pages(
    categories_page_1_html, categories_page_2_html, httpx_mock
):
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/group/?page=1",
        text=categories_page_1_html,
    )
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/group/?page=2",
        text=categories_page_2_html,
    )

    async with httpx.AsyncClient() as client:
        categories = await fetch_all_categories(client)
    assert len(categories) == 3
    slugs = [c.slug for c in categories]
    assert "agricultura" in slugs
    assert "educacion" in slugs
    assert "salud" in slugs


# ---------------------------------------------------------------------------
# API endpoint tests
# ---------------------------------------------------------------------------

MOCK_CATEGORIES = [
    Category(
        slug="agricultura",
        name="Agricultura",
        description="Datos sobre la actividad agrícola en México.",
        dataset_count=139,
        image_url="https://www.datos.gob.mx/uploads/group/agricultura.svg",
        url="https://www.datos.gob.mx/group/agricultura",
    ),
    Category(
        slug="educacion",
        name="Educación",
        description="Datos sobre el sistema educativo nacional.",
        dataset_count=1204,
        image_url="https://www.datos.gob.mx/uploads/group/educacion.svg",
        url="https://www.datos.gob.mx/group/educacion",
    ),
]


async def test_api_categories_endpoint():
    with patch(
        "open_data_mexico._scrapers.categories.fetch_all_categories",
        new=AsyncMock(return_value=MOCK_CATEGORIES),
    ):
        with patch.object(
            DatosGobMX, "get_categories", new=AsyncMock(return_value=MOCK_CATEGORIES)
        ):
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.get("/categories")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["categories"]) == 2
    assert data["categories"][0]["slug"] == "agricultura"


async def test_api_categories_slug_found():
    with patch.object(DatosGobMX, "get_categories", new=AsyncMock(return_value=MOCK_CATEGORIES)):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/categories/agricultura")

    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "agricultura"
    assert data["name"] == "Agricultura"
    assert data["dataset_count"] == 139


async def test_api_categories_slug_not_found():
    with patch.object(DatosGobMX, "get_categories", new=AsyncMock(return_value=MOCK_CATEGORIES)):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/categories/nonexistent")

    assert response.status_code == 404
    assert "nonexistent" in response.json()["detail"]


# ---------------------------------------------------------------------------
# New tests for DatosGobMX client
# ---------------------------------------------------------------------------


async def test_client_context_manager():
    async with DatosGobMX() as client:
        assert client._client is not None
    assert client._client is None


async def test_client_get_category_returns_none_when_not_found():
    with patch(
        "open_data_mexico.client.fetch_all_categories",
        new=AsyncMock(return_value=MOCK_CATEGORIES),
    ):
        async with DatosGobMX() as client:
            result = await client.get_category("nonexistent")
    assert result is None


def test_package_exports():
    import open_data_mexico

    assert hasattr(open_data_mexico, "DatosGobMX")
    assert hasattr(open_data_mexico, "Category")
    assert hasattr(open_data_mexico, "CategoriesResponse")
    # Version is sourced from importlib.metadata (pyproject.toml); just sanity-check the shape.
    assert isinstance(open_data_mexico.__version__, str)
    assert open_data_mexico.__version__.count(".") >= 1
