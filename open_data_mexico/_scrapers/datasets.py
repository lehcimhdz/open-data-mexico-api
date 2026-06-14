"""
Scraper for the per-category dataset listing pages at datos.gob.mx/group/{slug}.

Page structure (20 items per page):
  ul.dataset-list > li.resource-item   — one element per dataset
    h3 a.text-black[href]              — title and slug (/dataset/{slug})
    p > strong "Última Actualización:" — last-updated date string
    p > a.ms-1 "Ver base de datos"     — description paragraph (link removed)
    p > strong "Categoría:" > a[href]  — category name and slug
    a.link-pink[href]                  — organization name and slug
    p > strong "Número de bases..."    — resource file count

Pagination sits in ul.pagination; URL pattern: /group/{slug}?page={n}.
"""

import re
from collections.abc import AsyncGenerator

import httpx
from bs4 import BeautifulSoup

from open_data_mexico._config import BASE_URL, CONCURRENCY, MAX_RETRIES, REQUEST_DELAY
from open_data_mexico._http import gather_pages, robust_get
from open_data_mexico._utils import parse_spanish_date
from open_data_mexico.models import Dataset


def _parse_datasets_page(html: str) -> list[Dataset]:
    """Parse one page of a category's dataset listing.

    Args:
        html: Raw HTML of a ``/group/{slug}?page={n}`` response.

    Returns:
        List of Dataset objects found on that page (up to 20).
    """
    soup = BeautifulSoup(html, "lxml")
    datasets = []
    for item in soup.select("li.resource-item"):
        # slug and title from h3 a.text-black
        title_a = item.select_one("h3 a.text-black")
        if not title_a:
            continue
        href = str(title_a.get("href") or "")
        slug = href.rstrip("/").split("/")[-1]
        title = title_a.get_text(strip=True)
        url = BASE_URL + href if href.startswith("/") else href

        # last_updated: paragraph containing "Última Actualización:"
        last_updated = None
        for p in item.select("p"):
            strong = p.find("strong")
            if strong and "Última Actualización" in strong.get_text():
                text = p.get_text(separator=" ", strip=True)
                text = text.replace(strong.get_text(strip=True), "").strip().lstrip(":").strip()
                last_updated = parse_spanish_date(text)
                break

        # description: the p that contains "Ver base de datos" link
        description = None
        for p in item.select("p"):
            if p.find("a", class_="ms-1"):
                # Remove the "Ver base de datos" link text
                for a in p.find_all("a"):
                    a.decompose()
                description = p.get_text(strip=True) or None
                break

        # category: p containing "Categoría:" then an a[href*="/group/"]
        category_slug = None
        category_name = None
        for p in item.select("p"):
            strong = p.find("strong")
            if strong and "Categoría" in strong.get_text():
                cat_a = p.find("a")
                if cat_a:
                    cat_href = str(cat_a.get("href") or "")
                    category_slug = cat_href.rstrip("/").split("/")[-1]
                    category_name = cat_a.get_text(strip=True)
                break

        # organization: a.link-pink
        organization_slug = None
        organization_name = None
        org_a = item.select_one("a.link-pink")
        if org_a:
            org_href = str(org_a.get("href") or "")
            organization_slug = org_href.rstrip("/").split("/")[-1]
            organization_name = org_a.get_text(strip=True)

        # resource_count: p > strong containing "Número de bases de datos:"
        resource_count = None
        for p in item.select("p"):
            strong = p.find("strong")
            if strong and "Número de bases de datos" in strong.get_text():
                m = re.search(r"(\d[\d,]*)", strong.get_text())
                if m:
                    resource_count = int(m.group(1).replace(",", ""))
                break

        datasets.append(
            Dataset(
                slug=slug,
                title=title,
                last_updated=last_updated,
                description=description,
                category_slug=category_slug,
                category_name=category_name,
                organization_slug=organization_slug,
                organization_name=organization_name,
                resource_count=resource_count,
                url=url,
            )
        )
    return datasets


def _get_total_pages(html: str) -> int:
    """Return the total number of pages by reading the pagination widget.

    Scans all ``li`` elements inside ``ul.pagination`` — including active
    items (which may be ``span`` instead of ``a``) and disabled end caps —
    to avoid missing the last page when it is rendered as a non-link element.

    Args:
        html: Raw HTML of any ``/group/{slug}`` page.

    Returns:
        Maximum page number found in ``ul.pagination``, or 1 if no pagination.
    """
    soup = BeautifulSoup(html, "lxml")
    pages: set[int] = set()
    for li in soup.select("ul.pagination li"):
        text = li.get_text(strip=True)
        if text.isdigit():
            pages.add(int(text))
    # The site only renders a 1-2-3-…-N-1 N window; if a "next" link is still
    # present we don't actually know how many pages there are. Callers can use
    # :func:`_has_next_page` to drive an unbounded loop when needed.
    return max(pages) if pages else 1


def _has_next_page(html: str) -> bool:
    """Return True when the pagination widget still exposes a "next" link.

    datos.gob.mx renders a `<li class="next"><a ...>»</a></li>` element while
    there is a following page; it disappears (or gains ``.disabled``) on the
    last page. This lets us paginate past the visible numeric window for big
    categories like ``educacion`` (1430 datasets, but only the first 9 numeric
    pages are ever rendered).
    """
    soup = BeautifulSoup(html, "lxml")
    next_li = soup.select_one(
        "ul.pagination li.next, ul.pagination li.pagination-next"
    )
    if next_li is not None:
        classes = " ".join(next_li.get("class", []))
        if "disabled" in classes:
            return False
        return next_li.find("a") is not None
    # Some templates use rel="next" on the <a> directly without the wrapping li
    return soup.select_one('ul.pagination a[rel="next"]') is not None


async def fetch_category_datasets(
    client: httpx.AsyncClient,
    category_slug: str,
    *,
    request_delay: float = REQUEST_DELAY,
    max_retries: int = MAX_RETRIES,
    concurrency: int = CONCURRENCY,
) -> list[Dataset]:
    """Fetch all datasets for a category across all pages.

    Page 1 is fetched first to learn the total page count; remaining pages
    are fetched in parallel under a semaphore of size ``concurrency``.

    Args:
        client: An active ``httpx.AsyncClient`` with appropriate headers.
        category_slug: The category URL identifier, e.g. ``"seguridad"``.
        request_delay: Seconds to sleep after each successful request (rate limiting).
        max_retries: Retry attempts on transient failures.
        concurrency: Max number of pages fetched in parallel. Default 5.

    Returns:
        Combined list of all Dataset objects from every page, in site order
        (most recently updated first by default).

    Raises:
        httpx.HTTPStatusError: On non-2xx HTTP responses (404 if the slug
            does not match any category).
    """
    resp = await robust_get(
        client,
        f"{BASE_URL}/group/{category_slug}",
        request_delay=request_delay,
        max_retries=max_retries,
    )
    resp.raise_for_status()
    total_pages = _get_total_pages(resp.text)
    datasets = _parse_datasets_page(resp.text)
    last_html = resp.text

    if total_pages > 1:
        remaining = [
            (f"{BASE_URL}/group/{category_slug}", {"page": page})
            for page in range(2, total_pages + 1)
        ]
        responses = await gather_pages(
            client,
            remaining,
            concurrency=concurrency,
            max_retries=max_retries,
            request_delay=request_delay,
        )
        for r in responses:
            r.raise_for_status()
            datasets.extend(_parse_datasets_page(r.text))
            last_html = r.text

    # The pagination widget on datos.gob.mx only renders a narrow numeric
    # window (typically 1..9 even when 70+ pages exist), so we keep going past
    # the last visible page as long as the "next" link is still present.
    page = total_pages
    while _has_next_page(last_html):
        page += 1
        if page > 10_000:  # safety net — categories never get that big
            break
        resp = await robust_get(
            client,
            f"{BASE_URL}/group/{category_slug}",
            params={"page": page},
            request_delay=request_delay,
            max_retries=max_retries,
        )
        resp.raise_for_status()
        page_items = _parse_datasets_page(resp.text)
        if not page_items:
            break
        datasets.extend(page_items)
        last_html = resp.text

    return datasets


async def iter_category_datasets(
    client: httpx.AsyncClient,
    category_slug: str,
    *,
    request_delay: float = REQUEST_DELAY,
    max_retries: int = MAX_RETRIES,
) -> AsyncGenerator[Dataset, None]:
    """Yield datasets page-by-page for a category.

    Unlike :func:`fetch_category_datasets`, this is a streaming async
    generator: page 1 yields its datasets immediately, then each subsequent
    page is fetched sequentially so memory stays bounded and the caller can
    stop early without waiting for the full pagination.

    Args:
        client: An active ``httpx.AsyncClient`` with appropriate headers.
        category_slug: The category URL identifier, e.g. ``"seguridad"``.
        request_delay: Seconds to sleep after each successful request.
        max_retries: Retry attempts on transient failures.

    Yields:
        Each :class:`~open_data_mexico.models.Dataset` in page order.
    """
    resp = await robust_get(
        client,
        f"{BASE_URL}/group/{category_slug}",
        request_delay=request_delay,
        max_retries=max_retries,
    )
    resp.raise_for_status()
    total_pages = _get_total_pages(resp.text)
    for ds in _parse_datasets_page(resp.text):
        yield ds
    last_html = resp.text

    # First exhaust the numerically labelled pages (matches the original
    # behaviour and keeps the existing tests honest)…
    for page in range(2, total_pages + 1):
        resp = await robust_get(
            client,
            f"{BASE_URL}/group/{category_slug}",
            params={"page": page},
            request_delay=request_delay,
            max_retries=max_retries,
        )
        resp.raise_for_status()
        for ds in _parse_datasets_page(resp.text):
            yield ds
        last_html = resp.text

    # …then keep going as long as datos.gob.mx still advertises a "next"
    # link. The site truncates the numeric window to ~9 even when there are
    # 70+ pages, so for big categories this is the only way to reach the rest.
    page = total_pages
    while _has_next_page(last_html):
        page += 1
        if page > 10_000:  # safety net
            break
        resp = await robust_get(
            client,
            f"{BASE_URL}/group/{category_slug}",
            params={"page": page},
            request_delay=request_delay,
            max_retries=max_retries,
        )
        resp.raise_for_status()
        page_items = _parse_datasets_page(resp.text)
        if not page_items:
            break
        for ds in page_items:
            yield ds
        last_html = resp.text
