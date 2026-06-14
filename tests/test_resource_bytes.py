"""Tests for get_resource_bytes() and get_resource_dataframe()."""

from unittest.mock import patch

import pytest
from pytest_httpx import HTTPXMock

from open_data_mexico import DatosGobMX
from open_data_mexico.models import Resource

# ---------------------------------------------------------------------------
# get_resource_bytes
# ---------------------------------------------------------------------------


async def test_get_resource_bytes_returns_raw(httpx_mock: HTTPXMock):
    payload = b"\x00\x01\x02\x03some-binary-data"
    httpx_mock.add_response(url="https://example.com/blob.bin", content=payload)
    resource = Resource(
        resource_id="bin",
        name="blob",
        format="bin",
        download_url="https://example.com/blob.bin",
    )
    async with DatosGobMX() as client:
        result = await client.get_resource_bytes(resource)
    assert result == payload


async def test_get_resource_bytes_raises_without_url():
    resource = Resource(resource_id="x", name="x", download_url=None)
    async with DatosGobMX() as client:
        with pytest.raises(ValueError, match="no download_url"):
            await client.get_resource_bytes(resource)


async def test_get_resource_bytes_works_without_context_manager(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="https://example.com/x.bin", content=b"abc")
    resource = Resource(resource_id="x", name="x", download_url="https://example.com/x.bin")
    client = DatosGobMX()
    result = await client.get_resource_bytes(resource)
    assert result == b"abc"
    assert client._client is None  # cleaned up


# ---------------------------------------------------------------------------
# get_resource_dataframe
# ---------------------------------------------------------------------------


async def test_get_resource_dataframe_csv(httpx_mock: HTTPXMock):
    csv = "col1,col2\n1,2\n3,4\n"
    httpx_mock.add_response(url="https://example.com/data.csv", text=csv)
    resource = Resource(
        resource_id="csv",
        name="csv",
        format="csv",
        download_url="https://example.com/data.csv",
    )
    async with DatosGobMX() as client:
        df = await client.get_resource_dataframe(resource)
    assert list(df.columns) == ["col1", "col2"]
    assert df.shape == (2, 2)


async def test_get_resource_dataframe_csv_latin1_fallback(httpx_mock: HTTPXMock):
    raw = "año,nombre\n2025,José\n".encode("latin-1")
    httpx_mock.add_response(url="https://example.com/latin.csv", content=raw)
    resource = Resource(
        resource_id="csv",
        name="csv",
        format="csv",
        download_url="https://example.com/latin.csv",
    )
    async with DatosGobMX() as client:
        df = await client.get_resource_dataframe(resource)
    assert "año" in df.columns
    assert df.iloc[0, 1] == "José"


async def test_get_resource_dataframe_unsupported_format(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="https://example.com/x.shp", content=b"\x00")
    resource = Resource(
        resource_id="shp",
        name="shp",
        format="shp",
        download_url="https://example.com/x.shp",
    )
    async with DatosGobMX() as client:
        with pytest.raises(ValueError, match="Unsupported resource format"):
            await client.get_resource_dataframe(resource)


async def test_get_resource_dataframe_missing_pandas_raises():
    resource = Resource(
        resource_id="csv",
        name="csv",
        format="csv",
        download_url="https://example.com/data.csv",
    )

    with patch.dict("sys.modules", {"pandas": None}):
        async with DatosGobMX() as client:
            with pytest.raises(ImportError, match="pandas is required"):
                await client.get_resource_dataframe(resource)
