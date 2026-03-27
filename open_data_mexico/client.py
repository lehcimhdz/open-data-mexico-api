import httpx
from open_data_mexico._config import HEADERS
from open_data_mexico.models import Category, CategoriesResponse, Dataset
from open_data_mexico._scrapers.categories import fetch_all_categories

class DatosGobMX:
    """Async client for datos.gob.mx"""

    def __init__(self, timeout: float = 30.0):
        self._timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "DatosGobMX":
        self._client = httpx.AsyncClient(headers=HEADERS, timeout=self._timeout)
        return self

    async def __aexit__(self, *args) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    async def get_categories(self) -> list[Category]:
        """Fetch all categories from datos.gob.mx/group/"""
        client = self._client or httpx.AsyncClient(headers=HEADERS, timeout=self._timeout)
        try:
            return await fetch_all_categories(client)
        finally:
            if not self._client:
                await client.aclose()

    async def get_category(self, slug: str) -> Category | None:
        """Fetch a single category by slug. Returns None if not found."""
        categories = await self.get_categories()
        return next((c for c in categories if c.slug == slug), None)

    async def get_category_datasets(self, category_slug: str) -> list[Dataset]:
        """Fetch all datasets for a given category slug."""
        from open_data_mexico._scrapers.datasets import fetch_category_datasets
        client = self._client or httpx.AsyncClient(headers=HEADERS, timeout=self._timeout)
        try:
            return await fetch_category_datasets(client, category_slug)
        finally:
            if not self._client:
                await client.aclose()
