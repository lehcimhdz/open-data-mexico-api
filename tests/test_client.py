"""Tests for DatosGobMX client — cache behavior, standalone usage, and edge cases."""
from time import monotonic
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from pytest_httpx import HTTPXMock

from open_data_mexico import DatosGobMX
from open_data_mexico.models import Category, Organization, Resource


# ---------------------------------------------------------------------------
# _cache_get / _cache_set internals
# ---------------------------------------------------------------------------

class TestCacheGet:
    def test_returns_none_when_ttl_disabled(self):
        client = DatosGobMX(cache_ttl=0)
        # Manually insert an entry — _cache_get must still return None
        client._cache["key"] = (monotonic() + 100, "data")
        assert client._cache_get("key") is None

    def test_returns_data_when_fresh(self):
        client = DatosGobMX(cache_ttl=60)
        client._cache["key"] = (monotonic() + 60, "mydata")
        assert client._cache_get("key") == "mydata"

    def test_returns_none_when_expired_and_evicts_entry(self):
        client = DatosGobMX(cache_ttl=60)
        # Expiry in the past → stale
        client._cache["key"] = (monotonic() - 1, "stale")
        assert client._cache_get("key") is None
        assert "key" not in client._cache  # evicted

    def test_returns_none_for_missing_key(self):
        client = DatosGobMX(cache_ttl=60)
        assert client._cache_get("no-such-key") is None


class TestCacheSet:
    def test_stores_data_with_positive_ttl(self):
        client = DatosGobMX(cache_ttl=60)
        client._cache_set("key", "value")
        assert "key" in client._cache
        assert client._cache["key"][1] == "value"

    def test_noop_with_zero_ttl(self):
        client = DatosGobMX(cache_ttl=0)
        client._cache_set("key", "value")
        assert "key" not in client._cache


# ---------------------------------------------------------------------------
# get_categories — cache hit
# ---------------------------------------------------------------------------

class TestGetCategoriesCache:
    async def test_returns_cached_result_without_http(self):
        mock_cats = [Category(slug="a", name="A", url="https://x.com", dataset_count=1)]
        client = DatosGobMX(cache_ttl=60)
        client._cache_set("categories", mock_cats)

        with patch("open_data_mexico.client.fetch_all_categories") as mock_fetch:
            async with client:
                result = await client.get_categories()

        assert result == mock_cats
        mock_fetch.assert_not_called()


# ---------------------------------------------------------------------------
# get_category_datasets — cache hit
# ---------------------------------------------------------------------------

class TestGetCategoryDatasetsCache:
    async def test_returns_cached_datasets_without_http(self):
        from open_data_mexico.models import Dataset

        fake_datasets = [Dataset(slug="ds1", title="DS1", url="https://x.com")]
        client = DatosGobMX(cache_ttl=60)
        client._cache_set("datasets:economia", fake_datasets)

        with patch("open_data_mexico._scrapers.datasets.fetch_category_datasets") as mock_fetch:
            async with client:
                result = await client.get_category_datasets("economia")

        assert result == fake_datasets
        mock_fetch.assert_not_called()


# ---------------------------------------------------------------------------
# get_organizations — cache hit
# ---------------------------------------------------------------------------

class TestGetOrganizationsCache:
    async def test_returns_cached_organizations_without_http(self):
        fake_orgs = [Organization(slug="org1", title="Org 1", url="https://x.com", dataset_count=5)]
        client = DatosGobMX(cache_ttl=60)
        client._cache_set("organizations", fake_orgs)

        with patch("open_data_mexico._scrapers.organizations.fetch_all_organizations") as mock_fetch:
            async with client:
                result = await client.get_organizations()

        assert result == fake_orgs
        mock_fetch.assert_not_called()


# ---------------------------------------------------------------------------
# get_dataset — None result is not cached
# ---------------------------------------------------------------------------

class TestGetDatasetNotCached:
    async def test_none_result_not_stored_in_cache(self):
        from open_data_mexico._scrapers.dataset_detail import fetch_dataset_detail

        with patch(
            "open_data_mexico._scrapers.dataset_detail.fetch_dataset_detail",
            new=AsyncMock(return_value=None),
        ):
            async with DatosGobMX() as client:
                result = await client.get_dataset("nonexistent")

        assert result is None
        # 404 results must not be cached — repeated calls should always hit the network
        assert "dataset:nonexistent" not in client._cache


# ---------------------------------------------------------------------------
# get_resource_data — latin-1 fallback
# ---------------------------------------------------------------------------

class TestGetResourceDataEncoding:
    async def test_latin1_fallback_on_utf8_decode_error(self, httpx_mock: HTTPXMock):
        """Bytes that are invalid UTF-8 should be decoded with latin-1 fallback."""
        latin1_bytes = "año,código\nvalor1,valor2\n".encode("latin-1")
        httpx_mock.add_response(
            url="https://example.com/data.csv",
            content=latin1_bytes,
        )
        resource = Resource(
            resource_id="test",
            name="Test CSV",
            download_url="https://example.com/data.csv",
        )
        async with DatosGobMX() as client:
            data = await client.get_resource_data(resource)

        assert "valor1" in data
        assert "valor2" in data

    async def test_utf8_content_decoded_normally(self, httpx_mock: HTTPXMock):
        content = "col1,col2\nval1,val2\n"
        httpx_mock.add_response(
            url="https://example.com/utf8.csv",
            text=content,
        )
        resource = Resource(
            resource_id="utf8",
            name="UTF-8 CSV",
            download_url="https://example.com/utf8.csv",
        )
        async with DatosGobMX() as client:
            data = await client.get_resource_data(resource)

        assert "col1,col2" in data


# ---------------------------------------------------------------------------
# Standalone usage (no context manager) — exercises the finally cleanup branch
# ---------------------------------------------------------------------------

class TestStandaloneUsage:
    async def test_get_categories_without_context_manager(self, httpx_mock: HTTPXMock):
        from open_data_mexico._scrapers.categories import _parse_categories_page

        mock_categories = [Category(slug="salud", name="Salud", url="https://x.com", dataset_count=10)]
        with patch(
            "open_data_mexico.client.fetch_all_categories",
            new=AsyncMock(return_value=mock_categories),
        ):
            client = DatosGobMX()
            # No `async with` — must still work and close its own httpx client
            result = await client.get_categories()

        assert result == mock_categories
        # Internal client must have been closed (client._client is None after standalone call)
        assert client._client is None
