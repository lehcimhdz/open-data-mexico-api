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
import httpx
from bs4 import BeautifulSoup
from open_data_mexico._config import BASE_URL
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
        href = title_a.get("href", "")
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
                last_updated = text or None
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
                a = p.find("a")
                if a:
                    cat_href = a.get("href", "")
                    category_slug = cat_href.rstrip("/").split("/")[-1]
                    category_name = a.get_text(strip=True)
                break

        # organization: a.link-pink
        organization_slug = None
        organization_name = None
        org_a = item.select_one("a.link-pink")
        if org_a:
            org_href = org_a.get("href", "")
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

        datasets.append(Dataset(
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
        ))
    return datasets


def _get_total_pages(html: str) -> int:
    """Return the total number of pages by reading the pagination widget.

    Args:
        html: Raw HTML of any ``/group/{slug}`` page.

    Returns:
        Maximum page number found in ``ul.pagination``, or 1 if no pagination.
    """
    soup = BeautifulSoup(html, "lxml")
    pages = []
    for a in soup.select("ul.pagination li.page-item a.page-link"):
        text = a.get_text(strip=True)
        if text.isdigit():
            pages.append(int(text))
    return max(pages) if pages else 1


async def fetch_category_datasets(client: httpx.AsyncClient, category_slug: str) -> list[Dataset]:
    """Fetch all datasets for a category across all pages.

    Args:
        client: An active ``httpx.AsyncClient`` with appropriate headers.
        category_slug: The category URL identifier, e.g. ``"seguridad"``.

    Returns:
        Combined list of all Dataset objects from every page, in site order
        (most recently updated first by default).

    Raises:
        httpx.HTTPStatusError: On non-2xx HTTP responses (404 if the slug
            does not match any category).
    """
    resp = await client.get(f"{BASE_URL}/group/{category_slug}")
    resp.raise_for_status()
    total_pages = _get_total_pages(resp.text)
    datasets = _parse_datasets_page(resp.text)

    for page in range(2, total_pages + 1):
        resp = await client.get(f"{BASE_URL}/group/{category_slug}", params={"page": page})
        resp.raise_for_status()
        datasets.extend(_parse_datasets_page(resp.text))

    return datasets
