"""
Main async client for datos.gob.mx.

Typical usage — context manager (recommended, reuses one HTTP connection):

    async with DatosGobMX() as client:
        categories = await client.get_categories()
        datasets   = await client.get_category_datasets("seguridad")

One-shot usage (opens and closes a connection per call):

    client = DatosGobMX()
    categories = await client.get_categories()
"""

import httpx
from open_data_mexico._config import HEADERS
from open_data_mexico.models import Category, CategoriesResponse, Dataset
from open_data_mexico._scrapers.categories import fetch_all_categories


class DatosGobMX:
    """Async HTTP client for the datos.gob.mx open data portal.

    Can be used as an async context manager (preferred) or by calling
    methods directly. When used as a context manager, a single
    ``httpx.AsyncClient`` is shared across all requests, which is more
    efficient for multiple consecutive calls.

    Args:
        timeout: HTTP request timeout in seconds. Defaults to 30.

    Example::

        import asyncio
        from open_data_mexico import DatosGobMX

        async def main():
            async with DatosGobMX() as client:
                for cat in await client.get_categories():
                    print(cat.slug, cat.dataset_count)

        asyncio.run(main())
    """

    def __init__(self, timeout: float = 30.0) -> None:
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
        """Fetch every category from datos.gob.mx/group/.

        Automatically paginates through all pages (currently 2).

        Returns:
            A list of :class:`~open_data_mexico.models.Category` objects,
            one per category shown on the site (28 as of 2026).

        Raises:
            httpx.HTTPStatusError: If the server returns a non-2xx response.
            httpx.RequestError: On network-level failures (timeout, DNS, etc.).
        """
        client = self._client or httpx.AsyncClient(headers=HEADERS, timeout=self._timeout)
        try:
            return await fetch_all_categories(client)
        finally:
            if not self._client:
                await client.aclose()

    async def get_category(self, slug: str) -> Category | None:
        """Fetch a single category by its slug.

        Internally calls :meth:`get_categories` and filters the result,
        so it fetches all pages even when looking for one category.

        Args:
            slug: The URL identifier of the category, e.g. ``"seguridad"``
                  or ``"medio_ambiente"``.

        Returns:
            A :class:`~open_data_mexico.models.Category` if found,
            or ``None`` if no category matches the given slug.

        Raises:
            httpx.HTTPStatusError: If the server returns a non-2xx response.
            httpx.RequestError: On network-level failures (timeout, DNS, etc.).
        """
        categories = await self.get_categories()
        return next((c for c in categories if c.slug == slug), None)

    async def get_category_datasets(self, category_slug: str) -> list[Dataset]:
        """Fetch every dataset listed under a category.

        Automatically paginates through all pages of the category's
        dataset listing (e.g. ``/group/seguridad?page=2``).

        Args:
            category_slug: The URL identifier of the category, e.g.
                           ``"seguridad"``. Must match an existing category
                           slug; an invalid slug will raise an HTTP error.

        Returns:
            A list of :class:`~open_data_mexico.models.Dataset` objects
            in the order they appear on the site (most recently updated first
            by default).

        Raises:
            httpx.HTTPStatusError: If the server returns a non-2xx response
                (404 if the category slug does not exist).
            httpx.RequestError: On network-level failures (timeout, DNS, etc.).
        """
        from open_data_mexico._scrapers.datasets import fetch_category_datasets
        client = self._client or httpx.AsyncClient(headers=HEADERS, timeout=self._timeout)
        try:
            return await fetch_category_datasets(client, category_slug)
        finally:
            if not self._client:
                await client.aclose()
