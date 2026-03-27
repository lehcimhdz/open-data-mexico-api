import pytest
import httpx
from unittest.mock import AsyncMock, patch
from pytest_httpx import HTTPXMock

from open_data_mexico._scrapers.dataset_detail import _parse_dataset_detail, fetch_dataset_detail
from open_data_mexico.models import DatasetDetail, Resource
from open_data_mexico import DatosGobMX


async def test_parse_title(dataset_detail_html):
    detail = _parse_dataset_detail(dataset_detail_html, "expedientes_clasificados_ceav")
    assert detail.title == "Expedientes Clasificados CEAV"


async def test_parse_description(dataset_detail_html):
    detail = _parse_dataset_detail(dataset_detail_html, "expedientes_clasificados_ceav")
    assert detail.description and "reservados" in detail.description


async def test_parse_organization(dataset_detail_html):
    detail = _parse_dataset_detail(dataset_detail_html, "expedientes_clasificados_ceav")
    assert detail.organization_slug == "ceav"
    assert detail.organization_name and "CEAV" in detail.organization_name


async def test_parse_license(dataset_detail_html):
    detail = _parse_dataset_detail(dataset_detail_html, "expedientes_clasificados_ceav")
    assert detail.license_name == "Creative Commons Attribution 4.0"
    assert detail.license_url == "https://creativecommons.org/licenses/by/4.0/"


async def test_parse_tags(dataset_detail_html):
    detail = _parse_dataset_detail(dataset_detail_html, "expedientes_clasificados_ceav")
    assert len(detail.tags) == 13
    assert "transparencia" in detail.tags
    assert "expediente" in detail.tags
    assert "acceso información" in detail.tags
    assert "investigación" in detail.tags


async def test_parse_timestamps(dataset_detail_html):
    detail = _parse_dataset_detail(dataset_detail_html, "expedientes_clasificados_ceav")
    assert detail.created == "2026-03-23T16:28:17+0000"
    assert detail.last_updated == "2026-03-23T16:29:56+0000"


async def test_parse_resource_fields(dataset_detail_html):
    detail = _parse_dataset_detail(dataset_detail_html, "expedientes_clasificados_ceav")
    assert len(detail.resources) == 1
    r = detail.resources[0]
    assert r.resource_id == "c4b5b5e1-86df-482e-aa5e-466bef5e777f"
    assert r.name == "Índice de Expedientes Clasificados como Reservados"
    assert r.format == "csv"
    assert r.category_slug == "seguridad"
    assert r.category_name == "Seguridad"
    assert r.organization_slug == "ceav"
    assert r.organization_name == "Comisión Ejecutiva de Atención a Víctimas (CEAV)"
    assert r.download_url == "https://repodatos.atdt.gob.mx/api_update/ceav/expedientes_clasificados_ceav/Expedientes_clasificados_CEAV.csv"
    assert "expedientes_clasificados_ceav/resource/" in r.detail_url


async def test_parse_resource_description(dataset_detail_html):
    """Plain description paragraph is captured; labeled paragraphs (Categoría, Formatos, etc.) are not."""
    detail = _parse_dataset_detail(dataset_detail_html, "expedientes_clasificados_ceav")
    r = detail.resources[0]
    assert r.description is not None
    assert "expedientes" in r.description.lower()
    # Labeled fields must not bleed into the description
    assert "Categoría" not in r.description
    assert "Institución" not in r.description


async def test_fetch_dataset_returns_none_on_404(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/dataset/nonexistent",
        status_code=404,
        text="Not found"
    )
    async with httpx.AsyncClient() as client:
        result = await fetch_dataset_detail(client, "nonexistent")
    assert result is None


async def test_client_get_dataset(dataset_detail_html):
    fake_detail = DatasetDetail(
        slug="expedientes_clasificados_ceav",
        title="Expedientes Clasificados CEAV",
        url="https://www.datos.gob.mx/dataset/expedientes_clasificados_ceav",
    )
    with patch.object(DatosGobMX, "get_dataset", new=AsyncMock(return_value=fake_detail)):
        client = DatosGobMX()
        result = await client.get_dataset("expedientes_clasificados_ceav")
    assert result.slug == "expedientes_clasificados_ceav"


async def test_get_resource_data_no_url_raises():
    resource = Resource(
        resource_id="abc",
        name="Test",
        download_url=None,
    )
    client = DatosGobMX()
    try:
        await client.get_resource_data(resource)
        assert False, "Should have raised"
    except ValueError as e:
        assert "download_url" in str(e)


async def test_get_resource_data_streams_csv(httpx_mock: HTTPXMock):
    csv_content = "col1,col2\nval1,val2\n"
    httpx_mock.add_response(
        url="https://repodatos.atdt.gob.mx/test.csv",
        text=csv_content,
    )
    resource = Resource(
        resource_id="abc",
        name="Test CSV",
        download_url="https://repodatos.atdt.gob.mx/test.csv",
    )
    async with DatosGobMX() as client:
        data = await client.get_resource_data(resource)
    assert "col1,col2" in data
    assert "val1,val2" in data
