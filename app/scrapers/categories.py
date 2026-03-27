import re
import httpx
from bs4 import BeautifulSoup
from app.config import BASE_URL, HEADERS
from app.models.schemas import Category


async def _parse_categories_page(html: str) -> list[Category]:
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
    soup = BeautifulSoup(html, "lxml")
    pages = []
    for a in soup.select("ul.pagination li a"):
        text = a.get_text(strip=True)
        if text.isdigit():
            pages.append(int(text))
    return max(pages) if pages else 1


async def fetch_all_categories() -> list[Category]:
    async with httpx.AsyncClient(headers=HEADERS) as client:
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
