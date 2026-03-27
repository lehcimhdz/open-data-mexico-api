from unittest.mock import AsyncMock, patch

import httpx
from pytest_httpx import HTTPXMock

from open_data_mexico import DatosGobMX
from open_data_mexico._scrapers.dataset_detail import _parse_dataset_detail, fetch_dataset_detail
from open_data_mexico.models import DatasetDetail, Resource


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
    assert (
        r.download_url
        == "https://repodatos.atdt.gob.mx/api_update/ceav/expedientes_clasificados_ceav/Expedientes_clasificados_CEAV.csv"
    )
    assert "expedientes_clasificados_ceav/resource/" in r.detail_url


async def test_parse_resource_description(dataset_detail_html):
    """Plain description paragraph is captured; labeled paragraphs are not."""
    detail = _parse_dataset_detail(dataset_detail_html, "expedientes_clasificados_ceav")
    r = detail.resources[0]
    assert r.description is not None
    assert "expedientes" in r.description.lower()
    # Labeled fields must not bleed into the description
    assert "Categoría" not in r.description
    assert "Institución" not in r.description


async def test_fetch_dataset_returns_none_on_404(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/dataset/nonexistent", status_code=404, text="Not found"
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
        raise AssertionError("Should have raised ValueError")
    except ValueError as e:
        assert "download_url" in str(e)


async def test_prs_parse_title(dataset_detail_prs_html):
    slug = "cuaderno_mensual_estadistico_penitenciario_enero_2026"
    detail = _parse_dataset_detail(dataset_detail_prs_html, slug)
    assert detail.title == "Cuaderno Mensual Estadístico Penitenciario (enero, 2026)"


async def test_prs_parse_organization(dataset_detail_prs_html):
    slug = "cuaderno_mensual_estadistico_penitenciario_enero_2026"
    detail = _parse_dataset_detail(dataset_detail_prs_html, slug)
    assert detail.organization_slug == "prs"
    assert "Prevención y Reinserción Social" in detail.organization_name


async def test_prs_parse_description(dataset_detail_prs_html):
    slug = "cuaderno_mensual_estadistico_penitenciario_enero_2026"
    detail = _parse_dataset_detail(dataset_detail_prs_html, slug)
    assert detail.description and "privada de la libertad" in detail.description


async def test_prs_parse_multiple_resources(dataset_detail_prs_html):
    """Dataset with multiple resources: all are parsed and fields are independent."""
    slug = "cuaderno_mensual_estadistico_penitenciario_enero_2026"
    detail = _parse_dataset_detail(dataset_detail_prs_html, slug)
    assert len(detail.resources) == 3
    ids = [r.resource_id for r in detail.resources]
    assert "ba313dc7-391b-4900-9ec2-a475b5e46443" in ids
    assert "29c22724-a7ad-4d44-a11c-1a305111c6c2" in ids
    assert "aec4234c-ceaf-4551-a76d-9981235f8332" in ids
    # All resources belong to the same org and category
    for r in detail.resources:
        assert r.organization_slug == "prs"
        assert r.category_slug == "seguridad"
        assert r.format == "csv"
        assert r.download_url and "repodatos.atdt.gob.mx" in r.download_url
        assert r.description is not None


async def test_prs_resource_download_urls_are_distinct(dataset_detail_prs_html):
    slug = "cuaderno_mensual_estadistico_penitenciario_enero_2026"
    detail = _parse_dataset_detail(dataset_detail_prs_html, slug)
    urls = [r.download_url for r in detail.resources]
    assert len(urls) == len(set(urls)), "Each resource must have a unique download URL"


async def test_prs_parse_tags(dataset_detail_prs_html):
    slug = "cuaderno_mensual_estadistico_penitenciario_enero_2026"
    detail = _parse_dataset_detail(dataset_detail_prs_html, slug)
    assert len(detail.tags) == 11
    assert "centro penitenciario" in detail.tags
    assert "prisión" in detail.tags
    assert "sistema judicial" in detail.tags


async def test_prs_parse_timestamps(dataset_detail_prs_html):
    slug = "cuaderno_mensual_estadistico_penitenciario_enero_2026"
    detail = _parse_dataset_detail(dataset_detail_prs_html, slug)
    assert detail.created == "2026-03-09T21:40:15+0000"
    assert detail.last_updated == "2026-03-10T17:11:45+0000"


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


async def test_sesnsp_parse_title(dataset_detail_sesnsp_html):
    detail = _parse_dataset_detail(dataset_detail_sesnsp_html, "incidencia_delictiva")
    assert detail.title == "Incidencia delictiva"


async def test_sesnsp_parse_organization(dataset_detail_sesnsp_html):
    detail = _parse_dataset_detail(dataset_detail_sesnsp_html, "incidencia_delictiva")
    assert detail.organization_slug == "sesnsp"
    assert "SESNSP" in detail.organization_name


async def test_sesnsp_parse_description(dataset_detail_sesnsp_html):
    detail = _parse_dataset_detail(dataset_detail_sesnsp_html, "incidencia_delictiva")
    assert detail.description and "delictivos" in detail.description


async def test_sesnsp_parse_resources(dataset_detail_sesnsp_html):
    detail = _parse_dataset_detail(dataset_detail_sesnsp_html, "incidencia_delictiva")
    assert len(detail.resources) == 3
    ids = [r.resource_id for r in detail.resources]
    assert "d9b2792a-33a2-4ea8-8527-210d9e99de5e" in ids
    assert "57fbd692-3e5c-4b1b-8621-694cb3a33035" in ids
    assert "386f17d2-a488-4da2-9c85-99765b5a9cdc" in ids


async def test_sesnsp_visualizar_resource_has_detail_url(dataset_detail_sesnsp_html):
    """Resource with 'Visualizar' button still gets detail_url from the h3 link."""
    detail = _parse_dataset_detail(dataset_detail_sesnsp_html, "incidencia_delictiva")
    estatal = next(
        r for r in detail.resources if r.resource_id == "d9b2792a-33a2-4ea8-8527-210d9e99de5e"
    )
    assert estatal.detail_url and "incidencia_delictiva/resource/d9b2792a" in estatal.detail_url
    assert (
        estatal.download_url
        == "https://repodatos.atdt.gob.mx/api_update/sesnsp/incidencia_delictiva/INM_estatal_dic25.csv"
    )


async def test_sesnsp_parse_tags(dataset_detail_sesnsp_html):
    detail = _parse_dataset_detail(dataset_detail_sesnsp_html, "incidencia_delictiva")
    assert len(detail.tags) == 11
    assert "Feminicidio" in detail.tags
    assert "Homicidio doloso" in detail.tags
    assert "Extorsión" in detail.tags


async def test_sesnsp_parse_timestamps(dataset_detail_sesnsp_html):
    detail = _parse_dataset_detail(dataset_detail_sesnsp_html, "incidencia_delictiva")
    assert detail.created == "2025-03-13T23:27:31+0000"
    assert detail.last_updated == "2026-03-03T22:09:46+0000"
