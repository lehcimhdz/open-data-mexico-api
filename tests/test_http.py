"""Tests for open_data_mexico._http.robust_get.

Covers: success, non-retryable 4xx, retryable 5xx/429 (eventual success and
exhaustion), network-level errors (ConnectError, TimeoutException,
RemoteProtocolError), request_delay sleep, and query params forwarding.
"""

from unittest.mock import AsyncMock, patch

import httpx
import pytest
from pytest_httpx import HTTPXMock

from open_data_mexico._http import robust_get

_URL = "https://www.datos.gob.mx/test"


# ---------------------------------------------------------------------------
# Success path
# ---------------------------------------------------------------------------


async def test_success_returns_response(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=_URL, status_code=200, text="ok")
    async with httpx.AsyncClient() as client:
        resp = await robust_get(client, _URL)
    assert resp.status_code == 200
    assert resp.text == "ok"


async def test_non_retryable_404_returned_immediately(httpx_mock: HTTPXMock):
    """404 is not in _RETRYABLE_STATUS — must be returned directly without retry."""
    httpx_mock.add_response(url=_URL, status_code=404)
    async with httpx.AsyncClient() as client:
        resp = await robust_get(client, _URL)
    assert resp.status_code == 404


async def test_non_retryable_200_no_sleep_by_default(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=_URL, status_code=200, text="ok")
    with patch("open_data_mexico._http.asyncio.sleep", new=AsyncMock()) as mock_sleep:
        async with httpx.AsyncClient() as client:
            await robust_get(client, _URL, request_delay=0.0)
    mock_sleep.assert_not_called()


# ---------------------------------------------------------------------------
# request_delay
# ---------------------------------------------------------------------------


async def test_request_delay_sleeps_after_success(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=_URL, status_code=200, text="ok")
    with patch("open_data_mexico._http.asyncio.sleep", new=AsyncMock()) as mock_sleep:
        async with httpx.AsyncClient() as client:
            await robust_get(client, _URL, request_delay=0.5)
    mock_sleep.assert_called_once_with(0.5)


# ---------------------------------------------------------------------------
# Retryable HTTP status codes (5xx / 429)
# ---------------------------------------------------------------------------


async def test_retryable_500_retries_then_succeeds(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=_URL, status_code=500)
    httpx_mock.add_response(url=_URL, status_code=200, text="ok")
    with patch("open_data_mexico._http.asyncio.sleep", new=AsyncMock()):
        async with httpx.AsyncClient() as client:
            resp = await robust_get(client, _URL, max_retries=3)
    assert resp.status_code == 200


async def test_retryable_429_retries_then_succeeds(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=_URL, status_code=429)
    httpx_mock.add_response(url=_URL, status_code=200, text="ok")
    with patch("open_data_mexico._http.asyncio.sleep", new=AsyncMock()):
        async with httpx.AsyncClient() as client:
            resp = await robust_get(client, _URL, max_retries=3)
    assert resp.status_code == 200


async def test_retryable_502_exhausted_raises_http_status_error(httpx_mock: HTTPXMock):
    for _ in range(3):
        httpx_mock.add_response(url=_URL, status_code=502)
    with patch("open_data_mexico._http.asyncio.sleep", new=AsyncMock()):
        async with httpx.AsyncClient() as client:
            with pytest.raises(httpx.HTTPStatusError) as exc_info:
                await robust_get(client, _URL, max_retries=3)
    assert "502" in str(exc_info.value)


async def test_all_retryable_statuses_trigger_retry(httpx_mock: HTTPXMock):
    """503 and 504 are also in _RETRYABLE_STATUS."""
    for status in (503, 504):
        httpx_mock.add_response(url=_URL, status_code=status)
        httpx_mock.add_response(url=_URL, status_code=200, text="ok")
        with patch("open_data_mexico._http.asyncio.sleep", new=AsyncMock()):
            async with httpx.AsyncClient() as client:
                resp = await robust_get(client, _URL, max_retries=3)
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Network-level errors (ConnectError, TimeoutException, RemoteProtocolError)
# ---------------------------------------------------------------------------


async def test_connect_error_retries_then_succeeds(httpx_mock: HTTPXMock):
    httpx_mock.add_exception(httpx.ConnectError("refused"))
    httpx_mock.add_response(url=_URL, status_code=200, text="ok")
    with patch("open_data_mexico._http.asyncio.sleep", new=AsyncMock()):
        async with httpx.AsyncClient() as client:
            resp = await robust_get(client, _URL, max_retries=3)
    assert resp.status_code == 200


async def test_connect_error_exhausted_reraises(httpx_mock: HTTPXMock):
    for _ in range(2):
        httpx_mock.add_exception(httpx.ConnectError("refused"))
    with patch("open_data_mexico._http.asyncio.sleep", new=AsyncMock()):
        async with httpx.AsyncClient() as client:
            with pytest.raises(httpx.ConnectError):
                await robust_get(client, _URL, max_retries=2)


async def test_timeout_error_retries_then_succeeds(httpx_mock: HTTPXMock):
    httpx_mock.add_exception(httpx.ReadTimeout("timed out"))
    httpx_mock.add_response(url=_URL, status_code=200, text="ok")
    with patch("open_data_mexico._http.asyncio.sleep", new=AsyncMock()):
        async with httpx.AsyncClient() as client:
            resp = await robust_get(client, _URL, max_retries=3)
    assert resp.status_code == 200


async def test_remote_protocol_error_retries_then_succeeds(httpx_mock: HTTPXMock):
    httpx_mock.add_exception(httpx.RemoteProtocolError("bad frame"))
    httpx_mock.add_response(url=_URL, status_code=200, text="ok")
    with patch("open_data_mexico._http.asyncio.sleep", new=AsyncMock()):
        async with httpx.AsyncClient() as client:
            resp = await robust_get(client, _URL, max_retries=3)
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Backoff sleep
# ---------------------------------------------------------------------------


async def test_backoff_sleep_called_between_retries(httpx_mock: HTTPXMock):
    """asyncio.sleep is called with 2**attempt (2, 4, …) between retries."""
    httpx_mock.add_response(url=_URL, status_code=500)
    httpx_mock.add_response(url=_URL, status_code=500)
    httpx_mock.add_response(url=_URL, status_code=200, text="ok")
    with patch("open_data_mexico._http.asyncio.sleep", new=AsyncMock()) as mock_sleep:
        async with httpx.AsyncClient() as client:
            await robust_get(client, _URL, max_retries=3)
    # Attempt 0 → no sleep; attempt 1 → sleep(2); attempt 2 → sleep(4)
    calls = [c.args[0] for c in mock_sleep.call_args_list]
    assert 2 in calls
    assert 4 in calls


# ---------------------------------------------------------------------------
# Query params
# ---------------------------------------------------------------------------


async def test_passes_query_params(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=f"{_URL}?q=test&limit=5", status_code=200, text="ok")
    async with httpx.AsyncClient() as client:
        resp = await robust_get(client, _URL, params={"q": "test", "limit": 5})
    assert resp.status_code == 200
