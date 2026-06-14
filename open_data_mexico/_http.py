"""
Resilient HTTP helper for datos.gob.mx scraping.

Wraps httpx.AsyncClient.get() with:
- Exponential-backoff retry on 429/5xx responses and transient network errors.
- Optional configurable delay between every successful request (rate limiting).
"""

import asyncio
import logging
from collections.abc import Sequence

import httpx

from open_data_mexico._config import CONCURRENCY, MAX_RETRIES, REQUEST_DELAY

logger = logging.getLogger(__name__)

# HTTP status codes worth retrying (server-side transient failures).
_RETRYABLE_STATUS: frozenset[int] = frozenset({429, 500, 502, 503, 504})

# Network-level exceptions that warrant a retry.
_RETRYABLE_EXC = (
    httpx.ConnectError,
    httpx.TimeoutException,
    httpx.RemoteProtocolError,
)


async def robust_get(
    client: httpx.AsyncClient,
    url: str,
    *,
    params: dict | None = None,
    max_retries: int = MAX_RETRIES,
    request_delay: float = REQUEST_DELAY,
) -> httpx.Response:
    """GET a URL with automatic retry and optional rate-limit delay.

    Retries on 429/5xx status codes and transient network errors using
    exponential backoff (2 ^ attempt seconds between attempts).

    After each *successful* request, sleeps ``request_delay`` seconds so the
    caller can avoid hammering the remote server.

    Args:
        client: Active ``httpx.AsyncClient``.
        url: Absolute URL to fetch.
        params: Optional query parameters dict.
        max_retries: Total attempts before giving up (default 3).
        request_delay: Seconds to sleep after a successful response (default 0).

    Returns:
        The ``httpx.Response`` for the first non-retryable status code.

    Raises:
        httpx.HTTPStatusError: If all retries are exhausted on a 5xx/429.
        httpx.ConnectError / httpx.TimeoutException: If all retries fail on
            a network error.
    """
    last_exc: Exception | None = None

    for attempt in range(max_retries):
        if attempt > 0:
            backoff = 2**attempt  # 2s, 4s, 8s …
            logger.debug(
                "Retry %d/%d for %s — backing off %.0fs",
                attempt,
                max_retries - 1,
                url,
                backoff,
            )
            await asyncio.sleep(backoff)

        try:
            resp = await client.get(url, params=params)
        except _RETRYABLE_EXC as exc:
            last_exc = exc
            logger.warning("Network error (attempt %d/%d): %s", attempt + 1, max_retries, exc)
            continue

        if resp.status_code not in _RETRYABLE_STATUS:
            # Success (or a definitive 4xx like 404 — let caller handle it).
            if request_delay > 0:
                await asyncio.sleep(request_delay)
            return resp

        last_exc = httpx.HTTPStatusError(
            f"Server returned {resp.status_code}",
            request=resp.request,
            response=resp,
        )
        logger.warning(
            "Retryable status %d (attempt %d/%d) for %s",
            resp.status_code,
            attempt + 1,
            max_retries,
            url,
        )

    assert last_exc is not None
    raise last_exc


async def gather_pages(
    client: httpx.AsyncClient,
    requests: Sequence[tuple[str, dict | None]],
    *,
    concurrency: int = CONCURRENCY,
    max_retries: int = MAX_RETRIES,
    request_delay: float = REQUEST_DELAY,
) -> list[httpx.Response]:
    """Fetch many URLs in parallel while keeping result order.

    A bounded ``asyncio.Semaphore`` caps the number of in-flight requests at
    ``concurrency`` so we stay polite to the upstream site. Each individual
    request still goes through :func:`robust_get`, so retries, backoff and
    ``request_delay`` all apply per-page.

    Args:
        client: An active ``httpx.AsyncClient``.
        requests: Sequence of ``(url, params)`` tuples to fetch. ``params``
            may be ``None`` if the URL has no query string.
        concurrency: Max in-flight requests. Default 5.
        max_retries: Forwarded to :func:`robust_get`.
        request_delay: Forwarded to :func:`robust_get` — sleeps after each
            successful request inside its worker, not across workers.

    Returns:
        A list of :class:`httpx.Response` aligned with ``requests`` (same order).

    Raises:
        Whatever :func:`robust_get` raises — the first failing worker bubbles
        its exception out of ``asyncio.gather``.
    """
    if not requests:
        return []

    sem = asyncio.Semaphore(max(concurrency, 1))

    async def _one(url: str, params: dict | None) -> httpx.Response:
        async with sem:
            return await robust_get(
                client,
                url,
                params=params,
                max_retries=max_retries,
                request_delay=request_delay,
            )

    return await asyncio.gather(*(_one(url, params) for url, params in requests))
