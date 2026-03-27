"""
Scraper for government organizations via the CKAN JSON API.

  GET /api/3/action/organization_list  — all organizations (slug list or full objects)
  GET /api/3/action/organization_show  — single organization by slug
"""

import httpx

from open_data_mexico._config import BASE_URL, MAX_RETRIES, REQUEST_DELAY
from open_data_mexico._http import robust_get
from open_data_mexico._utils import parse_iso_dt
from open_data_mexico.models import Organization

_ORG_LIST_URL = f"{BASE_URL}/api/3/action/organization_list"
_ORG_SHOW_URL = f"{BASE_URL}/api/3/action/organization_show"


def _parse_org(data: dict) -> Organization:
    """Map a CKAN organization dict to an Organization model."""
    slug = data.get("name", "")
    return Organization(
        slug=slug,
        title=data.get("title") or data.get("display_name") or slug,
        description=data.get("description") or None,
        dataset_count=data.get("package_count", 0),
        image_url=data.get("image_display_url") or None,
        created=parse_iso_dt(data.get("created")),
        url=f"{BASE_URL}/organization/{slug}",
    )


async def fetch_all_organizations(
    client: httpx.AsyncClient,
    *,
    request_delay: float = REQUEST_DELAY,
    max_retries: int = MAX_RETRIES,
) -> list[Organization]:
    """Fetch all organizations from the CKAN API.

    Args:
        client: Active ``httpx.AsyncClient``.
        request_delay: Seconds to sleep after the request (rate limiting).
        max_retries: Retry attempts on transient failures.

    Returns:
        List of all Organization objects, sorted by slug.

    Raises:
        httpx.HTTPStatusError: On non-2xx API responses.
        ValueError: If the CKAN API returns ``success: false``.
    """
    resp = await robust_get(
        client,
        _ORG_LIST_URL,
        params={"all_fields": "true", "include_dataset_count": "true"},
        request_delay=request_delay,
        max_retries=max_retries,
    )
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise ValueError(f"CKAN API error: {body.get('error')}")
    return [_parse_org(o) for o in body["result"]]


async def fetch_organization(
    client: httpx.AsyncClient,
    slug: str,
    *,
    request_delay: float = REQUEST_DELAY,
    max_retries: int = MAX_RETRIES,
) -> Organization | None:
    """Fetch a single organization by slug.

    Args:
        client: Active ``httpx.AsyncClient``.
        slug: Organization identifier, e.g. ``'coneval'``.
        request_delay: Seconds to sleep after the request (rate limiting).
        max_retries: Retry attempts on transient failures.

    Returns:
        An Organization if found, or ``None`` if the slug does not exist.

    Raises:
        httpx.HTTPStatusError: On non-404 server errors.
    """
    resp = await robust_get(
        client,
        _ORG_SHOW_URL,
        params={"id": slug, "include_datasets": "false"},
        request_delay=request_delay,
        max_retries=max_retries,
    )
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        return None
    return _parse_org(body["result"])
