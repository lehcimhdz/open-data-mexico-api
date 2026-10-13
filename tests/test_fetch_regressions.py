"""Regression coverage for redirects, downloads, and upstream failures."""

from unittest.mock import AsyncMock, patch

import httpx
import pytest

from open_data_mexico import DatosGobMX
from open_data_mexico._http import robust_get
from open_data_mexico._scrapers.dataset_detail import _parse_dataset_detail
from open_data_mexico.models import Resource
from server.app import app


@pytest.mark.parametrize("use_context", [True, False])
async def test_download_follows_redirect_and_retries(httpx_mock, use_context):
    source = "https://example.com/data.csv"
    target = "https://example.com/files/data.csv"
    httpx_mock.add_response(url=source, status_code=302, headers={"Location": target})
    httpx_mock.add_response(url=target, status_code=503)
    httpx_mock.add_response(url=source, status_code=302, headers={"Location": target})
    httpx_mock.add_response(url=target, content=b"name\nMexico\n")
    resource = Resource(resource_id="test", name="test", download_url=source)
    client = DatosGobMX(max_retries=2, request_delay=0.1)
    with patch("open_data_mexico._http.asyncio.sleep", new=AsyncMock()) as sleep:
        if use_context:
            async with client:
                result = await client.get_resource_bytes(resource)
        else:
            result = await client.get_resource_bytes(resource)
    assert result == b"name\nMexico\n"
    assert [call.args[0] for call in sleep.call_args_list] == [2, 0.1]
    assert client._client is None


async def test_search_follows_redirect(httpx_mock):
    httpx_mock.add_response(
        status_code=307,
        headers={"Location": "https://www.datos.gob.mx/redirected-search"},
    )
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/redirected-search",
        json={"success": True, "result": {"count": 0, "results": []}},
    )
    async with DatosGobMX() as client:
        assert (await client.search("salud")).total == 0


def test_relative_download_url():
    html = """<ul class="resource-list"><li class="resource-item" data-id="test">
    <h3><a class="text-black">CSV</a></h3>
    <a class="btn-outline-primary" href="/files/data.csv">Descargar</a>
    </li></ul>"""
    detail = _parse_dataset_detail(html, "test")
    assert detail.resources[0].download_url == "https://www.datos.gob.mx/files/data.csv"


@pytest.mark.parametrize("attempts", [0, -1])
async def test_invalid_attempt_count(attempts):
    with pytest.raises(ValueError, match="max_retries"):
        DatosGobMX(max_retries=attempts)
    async with httpx.AsyncClient() as client:
        with pytest.raises(ValueError, match="max_retries"):
            await robust_get(client, "https://example.com", max_retries=attempts)


@pytest.mark.parametrize("failure, expected", [("403", 502), ("timeout", 504), ("network", 502)])
async def test_server_reports_upstream_failure(failure, expected):
    request = httpx.Request("GET", "https://www.datos.gob.mx/group/")
    if failure == "403":
        error = httpx.HTTPStatusError(
            "Access Denied", request=request, response=httpx.Response(403, request=request)
        )
    elif failure == "timeout":
        error = httpx.ReadTimeout("timed out", request=request)
    else:
        error = httpx.ConnectError("connection refused", request=request)
    with patch.object(DatosGobMX, "get_categories", new=AsyncMock(side_effect=error)):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/categories")
    assert response.status_code == expected
    if failure == "403":
        assert response.json()["upstream_status"] == 403
        assert "denied access" in response.json()["detail"]


@pytest.mark.parametrize("use_context", [True, False])
async def test_download_identifies_library_to_upstream(httpx_mock, use_context):
    """The old Chrome User-Agent reproduces the upstream CSV access denial."""
    url = "https://repodatos.atdt.gob.mx/api_update/cij/red_atencion/test.csv"

    def serve_csv(request):
        agent = request.headers.get("User-Agent", "")
        if agent != "open-data-mexico":
            return httpx.Response(403, text="Access Denied")
        return httpx.Response(200, content=b"id,name\n1,Centro\n")

    httpx_mock.add_callback(serve_csv, url=url)
    resource = Resource(resource_id="test", name="CSV", format="csv", download_url=url)
    client = DatosGobMX(max_retries=1)
    if use_context:
        async with client:
            result = await client.get_resource_data(resource)
    else:
        result = await client.get_resource_data(resource)
    assert result == "id,name\n1,Centro\n"
