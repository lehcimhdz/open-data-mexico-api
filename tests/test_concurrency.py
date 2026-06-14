"""Tests for the concurrent-pagination helper and propagation through scrapers."""

import asyncio
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from pytest_httpx import HTTPXMock

from open_data_mexico import DatosGobMX
from open_data_mexico._http import gather_pages
from open_data_mexico._scrapers.categories import fetch_all_categories
from open_data_mexico._scrapers.datasets import fetch_category_datasets

_URL_A = "https://www.datos.gob.mx/page-a"
_URL_B = "https://www.datos.gob.mx/page-b"
_URL_C = "https://www.datos.gob.mx/page-c"


# ---------------------------------------------------------------------------
# gather_pages — pure helper
# ---------------------------------------------------------------------------


async def test_gather_pages_empty_returns_empty():
    async with httpx.AsyncClient() as client:
        result = await gather_pages(client, [])
    assert result == []


async def test_gather_pages_preserves_order(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=_URL_A, text="A")
    httpx_mock.add_response(url=_URL_B, text="B")
    httpx_mock.add_response(url=_URL_C, text="C")

    async with httpx.AsyncClient() as client:
        responses = await gather_pages(
            client,
            [(_URL_A, None), (_URL_B, None), (_URL_C, None)],
            concurrency=3,
        )
    assert [r.text for r in responses] == ["A", "B", "C"]


async def test_gather_pages_respects_semaphore_cap(httpx_mock: HTTPXMock):
    """With concurrency=1 the semaphore must serialize requests."""
    in_flight = 0
    peak = 0
    gate = asyncio.Event()

    async def hook(request: httpx.Request) -> httpx.Response:
        nonlocal in_flight, peak
        in_flight += 1
        peak = max(peak, in_flight)
        # tiny await so the event loop has a chance to schedule siblings
        await asyncio.sleep(0)
        in_flight -= 1
        gate.set()
        return httpx.Response(200, text="ok")

    httpx_mock.add_callback(hook, url=_URL_A)
    httpx_mock.add_callback(hook, url=_URL_B)
    httpx_mock.add_callback(hook, url=_URL_C)

    async with httpx.AsyncClient() as client:
        await gather_pages(
            client,
            [(_URL_A, None), (_URL_B, None), (_URL_C, None)],
            concurrency=1,
        )
    assert peak == 1, f"semaphore did not serialize requests (peak={peak})"


async def test_gather_pages_propagates_errors(httpx_mock: HTTPXMock):
    """If a worker raises, gather() bubbles the exception up."""
    httpx_mock.add_response(url=_URL_A, text="ok")
    # Two retryable 502s without recovery → robust_get raises after exhaustion.
    for _ in range(3):
        httpx_mock.add_response(url=_URL_B, status_code=502)

    with patch("open_data_mexico._http.asyncio.sleep", new=AsyncMock()):
        async with httpx.AsyncClient() as client:
            with pytest.raises(httpx.HTTPStatusError):
                await gather_pages(
                    client,
                    [(_URL_A, None), (_URL_B, None)],
                    concurrency=2,
                    max_retries=3,
                )


# ---------------------------------------------------------------------------
# Concurrency propagation through the scrapers
# ---------------------------------------------------------------------------


def _fake_response(url: str, text: str) -> httpx.Response:
    """Build an httpx.Response with a Request attached so raise_for_status works."""
    return httpx.Response(200, text=text, request=httpx.Request("GET", url))


async def test_fetch_category_datasets_uses_concurrent_pagination():
    """When total_pages > 1 the scraper must delegate to gather_pages."""
    page_html = (
        "<html><body>"
        "<ul class='pagination'>"
        "<li>1</li><li>2</li><li>3</li>"
        "</ul>"
        "<ul class='dataset-list'></ul>"
        "</body></html>"
    )

    captured: dict = {}
    target_url = "https://www.datos.gob.mx/group/seguridad"

    async def fake_robust_get(client, url, *, params=None, max_retries=3, request_delay=0.0):
        return _fake_response(url, page_html)

    async def fake_gather_pages(client, requests, *, concurrency, max_retries, request_delay):
        captured["count"] = len(requests)
        captured["concurrency"] = concurrency
        return [_fake_response(target_url, page_html) for _ in requests]

    with patch(
        "open_data_mexico._scrapers.datasets.robust_get", new=AsyncMock(side_effect=fake_robust_get)
    ):
        with patch(
            "open_data_mexico._scrapers.datasets.gather_pages",
            new=AsyncMock(side_effect=fake_gather_pages),
        ):
            async with httpx.AsyncClient() as client:
                await fetch_category_datasets(client, "seguridad", concurrency=7)

    assert captured["count"] == 2  # pages 2 and 3
    assert captured["concurrency"] == 7


async def test_fetch_all_categories_uses_concurrent_pagination():
    """Same delegation check on the categories scraper."""
    page_html = (
        "<html><body>"
        "<ul class='pagination'>"
        "<li>1</li><li>2</li>"
        "</ul>"
        "<ul class='media-grid'></ul>"
        "</body></html>"
    )

    captured: dict = {}
    target_url = "https://www.datos.gob.mx/group/"

    async def fake_robust_get(client, url, *, params=None, max_retries=3, request_delay=0.0):
        return _fake_response(url, page_html)

    async def fake_gather_pages(client, requests, *, concurrency, max_retries, request_delay):
        captured["count"] = len(requests)
        captured["concurrency"] = concurrency
        return [_fake_response(target_url, page_html) for _ in requests]

    with patch(
        "open_data_mexico._scrapers.categories.robust_get",
        new=AsyncMock(side_effect=fake_robust_get),
    ):
        with patch(
            "open_data_mexico._scrapers.categories.gather_pages",
            new=AsyncMock(side_effect=fake_gather_pages),
        ):
            async with httpx.AsyncClient() as client:
                await fetch_all_categories(client, concurrency=3)

    assert captured["count"] == 1
    assert captured["concurrency"] == 3


async def test_client_propagates_concurrency_to_scrapers():
    """DatosGobMX(concurrency=N) must forward N to the scraper layer."""
    captured: dict = {}

    async def fake_fetch_all(client, *, request_delay, max_retries, concurrency):
        captured["concurrency"] = concurrency
        return []

    with patch(
        "open_data_mexico.client.fetch_all_categories", new=AsyncMock(side_effect=fake_fetch_all)
    ):
        async with DatosGobMX(concurrency=9) as client:
            await client.get_categories()

    assert captured["concurrency"] == 9
