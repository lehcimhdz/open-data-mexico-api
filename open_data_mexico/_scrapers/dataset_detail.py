"""
Scraper for individual dataset detail pages at datos.gob.mx/dataset/{slug}.

Page structure:
  h1.jumbotron-title                    — dataset title
  div.notes.embedded-content p          — description paragraph
  section#organization-info h1.heading  — organization display name
  section#organization-info img.item-image[alt] — organization slug
  section.license a[rel="dc:rights"]    — license name and URL
  ul.tag-list li a.tag                  — tags list
  section.additional-info table tbody tr — timestamps (Última actualización / Creado)

Per-resource (ul.resource-list li.resource-item):
  li[data-id]                           — resource UUID
  h3 a.text-black                       — resource name and detail page href
  p.mb-2 (no strong, no a.ms-1)        — plain description paragraph
  span[data-format]                     — file format (lowercase)
  a[href*="/group/"]                    — category slug and name
  a.link-pink                           — organization slug and name
  a.btn-outline-primary[href]           — download URL (Descargar button)
  a.btn-primary[href]                   — detail page href (Consultar button)
"""

import httpx
from bs4 import BeautifulSoup

from open_data_mexico._config import BASE_URL, MAX_RETRIES, REQUEST_DELAY
from open_data_mexico._http import robust_get
from open_data_mexico._utils import parse_iso_dt
from open_data_mexico.models import DatasetDetail, Resource


async def fetch_dataset_detail(
    client: httpx.AsyncClient,
    slug: str,
    *,
    request_delay: float = REQUEST_DELAY,
    max_retries: int = MAX_RETRIES,
) -> DatasetDetail | None:
    """Fetch full detail for a dataset by slug.

    Args:
        client: Active httpx.AsyncClient.
        slug: Dataset URL identifier, e.g. 'expedientes_clasificados_ceav'.
        request_delay: Seconds to sleep after each successful request (rate limiting).
        max_retries: Retry attempts on transient failures.

    Returns:
        DatasetDetail if the page exists, None if 404.

    Raises:
        httpx.HTTPStatusError: On non-404 HTTP errors.
    """
    resp = await robust_get(
        client,
        f"{BASE_URL}/dataset/{slug}",
        request_delay=request_delay,
        max_retries=max_retries,
    )
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return _parse_dataset_detail(resp.text, slug)


def _parse_dataset_detail(html: str, slug: str) -> DatasetDetail:
    """Parse the dataset detail HTML page into a DatasetDetail object."""
    soup = BeautifulSoup(html, "lxml")

    # title
    h1 = soup.select_one("h1.jumbotron-title")
    title = h1.get_text(strip=True) if h1 else slug

    # description
    desc_div = soup.select_one("div.notes.embedded-content")
    description = None
    if desc_div:
        p = desc_div.find("p")
        if p:
            description = p.get_text(strip=True) or None

    # organization
    org_section = soup.select_one("section#organization-info")
    organization_name = None
    organization_slug = None
    if org_section:
        h1_org = org_section.select_one("h1.heading")
        if h1_org:
            organization_name = h1_org.get_text(strip=True) or None
        # slug from img alt or from link href
        img = org_section.select_one("img.item-image")
        if img and img.get("alt"):
            organization_slug = str(img["alt"]).strip()
        if not organization_slug:
            a = org_section.select_one("a[href*='/organization/']")
            if a:
                organization_slug = str(a["href"]).rstrip("/").split("/")[-1]

    # license
    license_a = soup.select_one("section.license a[rel='dc:rights']")
    license_name = license_a.get_text(strip=True) if license_a else None
    license_url_raw = license_a.get("href") if license_a else None
    license_url = str(license_url_raw) if license_url_raw is not None else None

    # tags
    tags = [a.get_text(strip=True) for a in soup.select("ul.tag-list li a.tag")]

    # timestamps from additional-info table
    created = None
    last_updated = None
    for row in soup.select("section.additional-info table tbody tr"):
        th = row.find("th")
        if not th:
            continue
        label = th.get_text(strip=True)
        span = row.select_one("span.automatic-local-datetime")
        if not span:
            continue
        dt_raw = span.get("data-datetime")
        dt = str(dt_raw) if dt_raw is not None else None
        if "ltima actualizaci" in label or "Última" in label:
            last_updated = parse_iso_dt(dt)
        elif "Creado" in label:
            created = parse_iso_dt(dt)

    # resources
    resources = []
    for li in soup.select("ul.resource-list li.resource-item"):
        resource_id = str(li.get("data-id") or "")

        name_a = li.select_one("h3 a.text-black")
        name = name_a.get_text(strip=True) if name_a else ""
        detail_href = str(name_a.get("href") or "") if name_a else ""
        detail_url = (BASE_URL + detail_href) if detail_href.startswith("/") else detail_href

        # description: p without strong and without a.ms-1 (just plain text paragraph)
        resource_desc = None
        for p in li.select("p.mb-2"):
            if not p.find("strong") and not p.find("a", class_="ms-1"):
                txt = p.get_text(strip=True)
                if txt:
                    resource_desc = txt
                    break

        # format
        fmt_span = li.select_one("span[data-format]")
        fmt = str(fmt_span.get("data-format") or "").lower() if fmt_span else None

        # category
        cat_a = li.select_one("a[href*='/group/']")
        category_slug = None
        category_name = None
        if cat_a:
            category_slug = str(cat_a.get("href") or "").rstrip("/").split("/")[-1]
            category_name = cat_a.get_text(strip=True)

        # organization
        org_a = li.select_one("a.link-pink")
        res_org_slug = None
        res_org_name = None
        if org_a:
            res_org_slug = str(org_a.get("href") or "").rstrip("/").split("/")[-1]
            res_org_name = org_a.get_text(strip=True)

        # download URL (Descargar button)
        dl_a = li.select_one("a.btn-outline-primary")
        dl_href = dl_a.get("href") if dl_a else None
        download_url = str(dl_href) if dl_href is not None else None

        resources.append(
            Resource(
                resource_id=resource_id,
                name=name,
                description=resource_desc,
                format=fmt,
                category_slug=category_slug,
                category_name=category_name,
                organization_slug=res_org_slug,
                organization_name=res_org_name,
                download_url=download_url,
                detail_url=detail_url or None,
            )
        )

    return DatasetDetail(
        slug=slug,
        title=title,
        description=description,
        organization_slug=organization_slug,
        organization_name=organization_name,
        license_name=license_name,
        license_url=license_url,
        tags=tags,
        created=created,
        last_updated=last_updated,
        resources=resources,
        url=f"{BASE_URL}/dataset/{slug}",
    )
