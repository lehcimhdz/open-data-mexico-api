"""
Scraper for the categories listing pages at datos.gob.mx/group/.

Page structure (one page per 20 items, currently 2 pages total):
  ul.media-grid > li.media-item   — one element per category
    img.media-image[alt]          — slug (alt attr) and image URL (src attr)
    h2.media-heading              — display name
    p.media-description           — short description
    span.count                    — dataset count, e.g. "403 Bases de Datos"
    a.media-view[href]            — link to category page, href = /group/{slug}

Pagination sits in ul.pagination; pages are detected by reading the
maximum numeric link text.
"""

import re
import httpx
from bs4 import BeautifulSoup
from open_data_mexico._config import BASE_URL
from open_data_mexico.models import Category


async def _parse_categories_page(html: str) -> list[Category]:
    """Parse one page of the categories listing into a list of Category objects.

    Args:
        html: Raw HTML of a /group/?page={n} response.

    Returns:
        List of Category objects found on that page (up to 20).
    """
    soup = BeautifulSoup(html, "lxml")
    categories = []

    items = soup.select("ul.media-grid > li.media-item")
    for item in items:
        # slug
        img = item.select_one("img.media-image")
        slug = None
        if img and img.get("alt"):
            slug = img["alt"].strip()
        if not slug:
            a = item.select_one("a.media-view")
            if a and a.get("href"):
                slug = a["href"].rstrip("/").split("/")[-1]

        # name
        h2 = item.select_one("h2.media-heading")
        name = h2.get_text(strip=True) if h2 else ""

        # description
        p = item.select_one("p.media-description")
        description = p.get_text(strip=True) if p else None

        # dataset_count
        span = item.select_one("span.count")
        dataset_count = 0
        if span:
            text = span.get_text(strip=True)
            match = re.search(r"(\d[\d,]*)", text)
            if match:
                dataset_count = int(match.group(1).replace(",", ""))

        # image_url
        image_url = None
        if img and img.get("src"):
            src = img["src"]
            if src.startswith("https://"):
                image_url = src
            else:
                image_url = BASE_URL + src

        # url
        a = item.select_one("a.media-view")
        url = ""
        if a and a.get("href"):
            href = a["href"]
            if href.startswith("https://"):
                url = href
            else:
                url = BASE_URL + href

        if slug:
            categories.append(
                Category(
                    slug=slug,
                    name=name,
                    description=description,
                    dataset_count=dataset_count,
                    image_url=image_url,
                    url=url,
                )
            )

    return categories


async def _get_total_pages(html: str) -> int:
    """Return the total number of pages by reading the pagination widget.

    Args:
        html: Raw HTML of any /group/ page.

    Returns:
        Maximum page number found in ul.pagination, or 1 if no pagination.
    """
    soup = BeautifulSoup(html, "lxml")
    pages = []
    for a in soup.select("ul.pagination li a"):
        text = a.get_text(strip=True)
        if text.isdigit():
            pages.append(int(text))
    return max(pages) if pages else 1


async def fetch_all_categories(client: httpx.AsyncClient) -> list[Category]:
    """Fetch all categories across all pages.

    Fetches page 1 first to detect the total page count, then fetches
    any remaining pages concurrently (currently sequential, safe for rate limits).

    Args:
        client: An active ``httpx.AsyncClient`` with appropriate headers.

    Returns:
        Combined list of all Category objects from every page, in site order.

    Raises:
        httpx.HTTPStatusError: On non-2xx HTTP responses.
    """
    # Fetch first page to determine total pages
    resp = await client.get(f"{BASE_URL}/group/?page=1")
    resp.raise_for_status()
    first_page_html = resp.text

    total_pages = await _get_total_pages(first_page_html)
    all_categories = await _parse_categories_page(first_page_html)

    for page in range(2, total_pages + 1):
        resp = await client.get(f"{BASE_URL}/group/?page={page}")
        resp.raise_for_status()
        categories = await _parse_categories_page(resp.text)
        all_categories.extend(categories)

    return all_categories
