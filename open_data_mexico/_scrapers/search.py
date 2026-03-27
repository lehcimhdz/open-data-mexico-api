"""
Search datasets via the CKAN JSON API at datos.gob.mx/api/3/action/package_search.

Unlike the HTML scrapers, this module calls a structured JSON endpoint, so
results are already parsed — no BeautifulSoup required.

CKAN API reference:
  GET /api/3/action/package_search
  Parameters:
    q      — free-text query (Solr syntax supported)
    fq     — filter query, e.g. 'groups:seguridad'
    rows   — page size (default 20, max 1000)
    start  — offset for pagination
    sort   — e.g. 'metadata_modified desc'
"""

import httpx

from open_data_mexico._config import BASE_URL, MAX_RETRIES, REQUEST_DELAY
from open_data_mexico._http import robust_get
from open_data_mexico._utils import parse_iso_dt
from open_data_mexico.models import Dataset

_API_URL = f"{BASE_URL}/api/3/action/package_search"


def _parse_package(pkg: dict) -> Dataset:
    """Map a CKAN package dict to a Dataset model."""
    slug = pkg.get("name", "")
    groups = pkg.get("groups", [])
    org = pkg.get("organization") or {}

    return Dataset(
        slug=slug,
        title=pkg.get("title") or slug,
        last_updated=parse_iso_dt(pkg.get("metadata_modified")),
        description=pkg.get("notes") or None,
        category_slug=groups[0]["name"] if groups else None,
        category_name=groups[0].get("display_name") if groups else None,
        organization_slug=org.get("name") or None,
        organization_name=org.get("title") or None,
        resource_count=pkg.get("num_resources"),
        url=f"{BASE_URL}/dataset/{slug}",
    )


async def search_datasets(
    client: httpx.AsyncClient,
    query: str,
    *,
    category: str | None = None,
    limit: int = 20,
    offset: int = 0,
    request_delay: float = REQUEST_DELAY,
    max_retries: int = MAX_RETRIES,
) -> tuple[int, list[Dataset]]:
    """Search datasets via the CKAN API.

    Args:
        client: Active ``httpx.AsyncClient``.
        query: Free-text search term, e.g. ``"rezago social"``.
        category: Optional category slug to restrict results, e.g. ``"salud"``.
        limit: Maximum number of results to return (default 20, max 1 000).
        offset: Number of results to skip for pagination (default 0).
        request_delay: Seconds to sleep after the request (rate limiting).
        max_retries: Retry attempts on transient failures.

    Returns:
        A tuple of ``(total, datasets)`` where *total* is the number of
        matching datasets on the portal and *datasets* is the current page.

    Raises:
        httpx.HTTPStatusError: On non-2xx API responses.
        httpx.RequestError: On network failures.
        ValueError: If the CKAN API returns ``success: false``.
    """
    params: dict[str, str | int] = {
        "q": query,
        "rows": limit,
        "start": offset,
        "sort": "metadata_modified desc",
    }
    if category:
        params["fq"] = f"groups:{category}"

    resp = await robust_get(
        client,
        _API_URL,
        params=params,
        request_delay=request_delay,
        max_retries=max_retries,
    )
    resp.raise_for_status()

    body = resp.json()
    if not body.get("success"):
        raise ValueError(f"CKAN API error: {body.get('error')}")

    result = body["result"]
    total: int = result["count"]
    datasets = [_parse_package(pkg) for pkg in result["results"]]
    return total, datasets
