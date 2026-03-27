"""
Main async client for datos.gob.mx.

Typical usage — context manager (recommended, reuses one HTTP connection):

    async with DatosGobMX() as client:
        categories = await client.get_categories()
        datasets   = await client.get_category_datasets("seguridad")

One-shot usage (opens and closes a connection per call):

    client = DatosGobMX()
    categories = await client.get_categories()

Rate limiting (avoid hammering the site):

    async with DatosGobMX(request_delay=0.5) as client:
        ...
"""

from time import monotonic
from typing import Any, cast

import httpx

from open_data_mexico._config import CACHE_TTL, HEADERS, MAX_RETRIES, REQUEST_DELAY
from open_data_mexico._scrapers.categories import fetch_all_categories
from open_data_mexico.models import (
    Category,
    Dataset,
    DatasetDetail,
    Organization,
    Resource,
    SearchResponse,
)


class DatosGobMX:
    """Async HTTP client for the datos.gob.mx open data portal.

    Can be used as an async context manager (preferred) or by calling
    methods directly. When used as a context manager, a single
    ``httpx.AsyncClient`` is shared across all requests, which is more
    efficient for multiple consecutive calls.

    Args:
        timeout: HTTP request timeout in seconds. Defaults to 30.
        request_delay: Seconds to wait between requests. Increase to avoid
            hammering the site (e.g. ``0.5``). Defaults to 0 (no delay).
        max_retries: Number of retry attempts on transient 5xx/429 or
            network failures. Defaults to 3.
        cache_ttl: Seconds to keep responses in memory. Set to ``0`` to
            disable caching. Defaults to 300 (5 minutes).

    Example::

        import asyncio
        from open_data_mexico import DatosGobMX

        async def main():
            async with DatosGobMX(request_delay=0.5) as client:
                for cat in await client.get_categories():
                    print(cat.slug, cat.dataset_count)

        asyncio.run(main())
    """

    def __init__(
        self,
        timeout: float = 30.0,
        request_delay: float = REQUEST_DELAY,
        max_retries: int = MAX_RETRIES,
        cache_ttl: float = CACHE_TTL,
    ) -> None:
        self._timeout = timeout
        self._request_delay = request_delay
        self._max_retries = max_retries
        self._cache_ttl = cache_ttl
        self._cache: dict[str, tuple[float, Any]] = {}
        self._client: httpx.AsyncClient | None = None

    # ------------------------------------------------------------------
    # Internal cache helpers
    # ------------------------------------------------------------------

    def _cache_get(self, key: str) -> Any | None:
        """Return cached value for *key* if still fresh, else None."""
        if self._cache_ttl <= 0:
            return None
        entry = self._cache.get(key)
        if entry is None:
            return None
        expiry, data = entry
        if monotonic() < expiry:
            return data
        del self._cache[key]
        return None

    def _cache_set(self, key: str, data: Any) -> None:
        """Store *data* under *key* with the configured TTL."""
        if self._cache_ttl > 0:
            self._cache[key] = (monotonic() + self._cache_ttl, data)

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
        Results are cached in memory for ``cache_ttl`` seconds.

        Returns:
            A list of :class:`~open_data_mexico.models.Category` objects,
            one per category shown on the site (28 as of 2026).

        Raises:
            httpx.HTTPStatusError: If the server returns a non-2xx response.
            httpx.RequestError: On network-level failures (timeout, DNS, etc.).
        """
        cached = self._cache_get("categories")
        if cached is not None:
            return cast(list[Category], cached)

        client = self._client or httpx.AsyncClient(headers=HEADERS, timeout=self._timeout)
        try:
            result = await fetch_all_categories(
                client,
                request_delay=self._request_delay,
                max_retries=self._max_retries,
            )
        finally:
            if not self._client:
                await client.aclose()

        self._cache_set("categories", result)
        return result

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
        Results are cached in memory for ``cache_ttl`` seconds.

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

        cache_key = f"datasets:{category_slug}"
        cached = self._cache_get(cache_key)
        if cached is not None:
            return cast(list[Dataset], cached)

        client = self._client or httpx.AsyncClient(headers=HEADERS, timeout=self._timeout)
        try:
            result = await fetch_category_datasets(
                client,
                category_slug,
                request_delay=self._request_delay,
                max_retries=self._max_retries,
            )
        finally:
            if not self._client:
                await client.aclose()

        self._cache_set(cache_key, result)
        return result

    async def get_dataset(self, slug: str) -> DatasetDetail | None:
        """Fetch the full detail page for a dataset.

        Args:
            slug: Dataset URL identifier, e.g. 'expedientes_clasificados_ceav'.

        Returns:
            A DatasetDetail with all resources, tags, timestamps, etc.
            Returns None if the dataset does not exist (404).

        Raises:
            httpx.HTTPStatusError: On non-404 server errors.
            httpx.RequestError: On network failures.
        """
        from open_data_mexico._scrapers.dataset_detail import fetch_dataset_detail

        cache_key = f"dataset:{slug}"
        cached = self._cache_get(cache_key)
        if cached is not None:
            return cast(DatasetDetail, cached)

        client = self._client or httpx.AsyncClient(headers=HEADERS, timeout=self._timeout)
        try:
            result = await fetch_dataset_detail(
                client,
                slug,
                request_delay=self._request_delay,
                max_retries=self._max_retries,
            )
        finally:
            if not self._client:
                await client.aclose()

        if result is not None:
            self._cache_set(cache_key, result)
        return result

    async def get_resource_data(self, resource: Resource) -> str:
        """Download a resource file into memory as a string — no disk writes.

        Streams the raw file content (typically CSV) over HTTP and returns it
        as a Python string. The data is never written to disk.

        Use ``io.StringIO`` to parse the result with pandas or the csv module:

            import io, pandas as pd
            data = await client.get_resource_data(resource)
            df = pd.read_csv(io.StringIO(data))

        Or with the built-in csv module (no extra dependencies):

            import io, csv
            reader = csv.DictReader(io.StringIO(data))
            rows = list(reader)

        Args:
            resource: A Resource object with a non-None download_url.

        Returns:
            The raw file content as a UTF-8 string (falls back to latin-1
            if UTF-8 decoding fails, which is common with Mexican government
            CSV files).

        Raises:
            ValueError: If resource.download_url is None.
            httpx.HTTPStatusError: On non-2xx HTTP responses.
            httpx.RequestError: On network failures.
        """
        if not resource.download_url:
            raise ValueError(f"Resource '{resource.name}' has no download_url.")
        client = self._client or httpx.AsyncClient(headers=HEADERS, timeout=self._timeout)
        try:
            resp = await client.get(resource.download_url)
            resp.raise_for_status()
            # Many Mexican gov CSV files use latin-1 encoding
            try:
                return resp.content.decode("utf-8")
            except UnicodeDecodeError:
                return resp.content.decode("latin-1")
        finally:
            if not self._client:
                await client.aclose()

    async def search(
        self,
        query: str,
        *,
        category: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> SearchResponse:
        """Search datasets by keyword using the CKAN JSON API.

        Unlike :meth:`get_category_datasets`, this searches across all
        categories and returns results ranked by relevance (most recently
        updated first). Results are **not** cached because search queries
        are too varied to benefit from a shared TTL cache.

        Args:
            query: Free-text search term, e.g. ``"rezago social"`` or
                   ``"incidencia delictiva"``.
            category: Optional category slug to restrict results,
                      e.g. ``"salud"``. When provided only datasets in
                      that category are returned.
            limit: Maximum number of results per page (default 20, max 1 000).
            offset: Number of results to skip — use with ``limit`` to paginate
                    through large result sets.

        Returns:
            A :class:`~open_data_mexico.models.SearchResponse` with the
            ``total`` count of matching datasets on the portal plus the
            current page of :class:`~open_data_mexico.models.Dataset` objects.

        Raises:
            httpx.HTTPStatusError: On non-2xx API responses.
            httpx.RequestError: On network failures.
            ValueError: If the CKAN API returns an error response.

        Example::

            async with DatosGobMX() as client:
                resp = await client.search("rezago social")
                print(resp.total, "datasets encontrados")
                for ds in resp.datasets:
                    print(ds.title, ds.organization_name)

                # Paginar
                page2 = await client.search("salud", limit=20, offset=20)

                # Filtrar por categoría
                result = await client.search("mortalidad", category="salud")
        """
        from open_data_mexico._scrapers.search import search_datasets

        client = self._client or httpx.AsyncClient(headers=HEADERS, timeout=self._timeout)
        try:
            total, datasets = await search_datasets(
                client,
                query,
                category=category,
                limit=limit,
                offset=offset,
                request_delay=self._request_delay,
                max_retries=self._max_retries,
            )
        finally:
            if not self._client:
                await client.aclose()

        return SearchResponse(
            total=total,
            query=query,
            category=category,
            offset=offset,
            datasets=datasets,
        )

    async def get_organizations(self) -> list[Organization]:
        """Fetch all government organizations that publish datasets.

        Uses the CKAN API (``/api/3/action/organization_list``). Results are
        cached in memory for ``cache_ttl`` seconds.

        Returns:
            List of :class:`~open_data_mexico.models.Organization` objects
            sorted alphabetically by slug (184 organizations as of 2026).

        Raises:
            httpx.HTTPStatusError: On non-2xx API responses.
            httpx.RequestError: On network failures.
        """
        from open_data_mexico._scrapers.organizations import fetch_all_organizations

        cached = self._cache_get("organizations")
        if cached is not None:
            return cast(list[Organization], cached)

        client = self._client or httpx.AsyncClient(headers=HEADERS, timeout=self._timeout)
        try:
            result = await fetch_all_organizations(
                client,
                request_delay=self._request_delay,
                max_retries=self._max_retries,
            )
        finally:
            if not self._client:
                await client.aclose()

        self._cache_set("organizations", result)
        return result

    async def get_organization(self, slug: str) -> Organization | None:
        """Fetch a single organization by slug.

        Args:
            slug: Organization identifier, e.g. ``'coneval'`` or ``'imss'``.

        Returns:
            An :class:`~open_data_mexico.models.Organization` if found,
            or ``None`` if the slug does not exist.

        Raises:
            httpx.HTTPStatusError: On non-404 server errors.
            httpx.RequestError: On network failures.
        """
        from open_data_mexico._scrapers.organizations import fetch_organization

        client = self._client or httpx.AsyncClient(headers=HEADERS, timeout=self._timeout)
        try:
            return await fetch_organization(
                client,
                slug,
                request_delay=self._request_delay,
                max_retries=self._max_retries,
            )
        finally:
            if not self._client:
                await client.aclose()
