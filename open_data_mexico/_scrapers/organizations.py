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


# datos.gob.mx's CKAN ignores the `limit` parameter on organization_list and
# always returns 25 rows. We still send a generous `limit` so a more sensible
# CKAN install could give us bigger pages, but we drive pagination off the
# actual page size and the presence of more rows at `offset = total`.
_ORG_LIST_PAGE_SIZE = 1000


async def fetch_all_organizations(
    client: httpx.AsyncClient,
    *,
    request_delay: float = REQUEST_DELAY,
    max_retries: int = MAX_RETRIES,
) -> list[Organization]:
    """Fetch all organizations from the CKAN API.

    Paginates using ``offset`` until an empty page comes back. This works
    even on CKAN installs that cap the response well below the requested
    ``limit`` (datos.gob.mx returns 25 regardless of what we ask for).

    Args:
        client: Active ``httpx.AsyncClient``.
        request_delay: Seconds to sleep after each request (rate limiting).
        max_retries: Retry attempts on transient failures.

    Returns:
        List of every Organization the server is willing to show.

    Raises:
        httpx.HTTPStatusError: On non-2xx API responses.
        ValueError: If the CKAN API returns ``success: false``.
    """
    all_orgs: list[Organization] = []
    offset = 0
    while True:
        resp = await robust_get(
            client,
            _ORG_LIST_URL,
            params={
                "all_fields": "true",
                "include_dataset_count": "true",
                "limit": _ORG_LIST_PAGE_SIZE,
                "offset": offset,
            },
            request_delay=request_delay,
            max_retries=max_retries,
        )
        resp.raise_for_status()
        body = resp.json()
        if not body.get("success"):
            raise ValueError(f"CKAN API error: {body.get('error')}")
        page = body["result"]
        if not page:
            break
        all_orgs.extend(_parse_org(o) for o in page)
        offset += len(page)
        if offset > 100_000:  # safety net
            break
    return all_orgs


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
