"""
open-data-mexico — Unofficial Python client for datos.gob.mx.

This library scrapes the public HTML pages of the Mexican government's
open data portal (https://www.datos.gob.mx/) and exposes the results
as typed Python objects.

Public API surface
------------------
:class:`DatosGobMX`
    Async context-manager client. Entry point for all data access.

:class:`Category`
    A thematic category (e.g. "Seguridad", "Salud").

:class:`Dataset`
    A dataset card listed under a category page.

:class:`CategoriesResponse`
    REST-server wrapper around a list of categories.

:class:`DatasetsResponse`
    REST-server wrapper around a list of datasets.

:class:`Resource`
    A single downloadable resource file attached to a dataset.

:class:`DatasetDetail`
    Full detail of a dataset page including all resources and metadata.

:class:`SearchResponse`
    Result of a keyword search via the CKAN API.

Quick start::

    import asyncio
    from open_data_mexico import DatosGobMX

    async def main():
        async with DatosGobMX() as client:
            categories = await client.get_categories()
            datasets   = await client.get_category_datasets("seguridad")
            detail     = await client.get_dataset("expedientes_clasificados_ceav")

    asyncio.run(main())
"""

from open_data_mexico.client import DatosGobMX
from open_data_mexico.models import (
    CategoriesResponse,
    Category,
    Dataset,
    DatasetDetail,
    DatasetsResponse,
    Organization,
    OrganizationsResponse,
    Resource,
    SearchResponse,
)

__version__ = "0.1.0"
__all__ = [
    "DatosGobMX",
    "Category",
    "CategoriesResponse",
    "Dataset",
    "DatasetDetail",
    "DatasetsResponse",
    "Organization",
    "OrganizationsResponse",
    "Resource",
    "SearchResponse",
]
