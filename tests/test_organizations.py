from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

import httpx

from open_data_mexico import DatosGobMX
from open_data_mexico._scrapers.organizations import _parse_org, fetch_organization
from server.app import app

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

CKAN_ORG = {
    "name": "coneval",
    "title": "Consejo Nacional de Evaluación de la Política de Desarrollo Social (CONEVAL)",
    "display_name": "CONEVAL",
    "description": "Organismo autónomo que mide la pobreza en México.",
    "package_count": 2,
    "image_display_url": "https://www.datos.gob.mx/uploads/group/coneval.png",
    "created": "2015-03-01T00:00:00.000000",
}

CKAN_ORG_LIST_RESPONSE = {
    "success": True,
    "result": [CKAN_ORG],
}

CKAN_ORG_SHOW_RESPONSE = {
    "success": True,
    "result": CKAN_ORG,
}


# ---------------------------------------------------------------------------
# Unit tests — _parse_org
# ---------------------------------------------------------------------------


def test_parse_org_maps_fields():
    org = _parse_org(CKAN_ORG)
    assert org.slug == "coneval"
    assert "CONEVAL" in org.title
    assert org.description == "Organismo autónomo que mide la pobreza en México."
    assert org.dataset_count == 2
    assert org.image_url == "https://www.datos.gob.mx/uploads/group/coneval.png"
    assert org.created == datetime(2015, 3, 1, tzinfo=UTC)
    assert org.url == "https://www.datos.gob.mx/organization/coneval"


def test_parse_org_no_description():
    org = _parse_org({**CKAN_ORG, "description": ""})
    assert org.description is None


def test_parse_org_no_image():
    org = _parse_org({**CKAN_ORG, "image_display_url": None})
    assert org.image_url is None


# ---------------------------------------------------------------------------
# Integration tests — fetch_organization (httpx_mock)
# ---------------------------------------------------------------------------


async def test_fetch_organization_found(httpx_mock):
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/api/3/action/organization_show?id=coneval&include_datasets=false",
        json=CKAN_ORG_SHOW_RESPONSE,
    )
    async with httpx.AsyncClient() as client:
        org = await fetch_organization(client, "coneval")
    assert org is not None
    assert org.slug == "coneval"


async def test_fetch_organization_not_found(httpx_mock):
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/api/3/action/organization_show?id=nope&include_datasets=false",
        status_code=404,
    )
    async with httpx.AsyncClient() as client:
        org = await fetch_organization(client, "nope")
    assert org is None


# ---------------------------------------------------------------------------
# Client integration — DatosGobMX
# ---------------------------------------------------------------------------


async def test_client_get_organizations():
    mock_orgs = [_parse_org(CKAN_ORG)]
    with patch(
        "open_data_mexico._scrapers.organizations.fetch_all_organizations",
        new=AsyncMock(return_value=mock_orgs),
    ):
        async with DatosGobMX() as client:
            result = await client.get_organizations()
    assert len(result) == 1
    assert result[0].slug == "coneval"


async def test_client_get_organization_found():
    mock_org = _parse_org(CKAN_ORG)
    with patch(
        "open_data_mexico._scrapers.organizations.fetch_organization",
        new=AsyncMock(return_value=mock_org),
    ):
        async with DatosGobMX() as client:
            org = await client.get_organization("coneval")
    assert org is not None
    assert org.dataset_count == 2


async def test_client_get_organization_not_found():
    with patch(
        "open_data_mexico._scrapers.organizations.fetch_organization",
        new=AsyncMock(return_value=None),
    ):
        async with DatosGobMX() as client:
            org = await client.get_organization("nope")
    assert org is None


# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------


async def test_api_list_organizations():
    mock_resp = [_parse_org(CKAN_ORG)]
    with patch.object(DatosGobMX, "get_organizations", new=AsyncMock(return_value=mock_resp)):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/organizations")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["organizations"][0]["slug"] == "coneval"


async def test_api_get_organization_found():
    mock_org = _parse_org(CKAN_ORG)
    with patch.object(DatosGobMX, "get_organization", new=AsyncMock(return_value=mock_org)):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/organizations/coneval")

    assert response.status_code == 200
    assert response.json()["slug"] == "coneval"


async def test_api_get_organization_not_found():
    with patch.object(DatosGobMX, "get_organization", new=AsyncMock(return_value=None)):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/organizations/nope")

    assert response.status_code == 404
