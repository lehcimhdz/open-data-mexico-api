"""
Pydantic models representing data scraped from datos.gob.mx.

All models are read-only data containers. Field values are extracted
from the site's public HTML pages and reflect whatever the site
currently publishes — no transformations beyond basic text cleanup.
"""

from pydantic import BaseModel, Field
from typing import Optional


class Category(BaseModel):
    """A thematic category grouping datasets on datos.gob.mx.

    Categories are listed at https://www.datos.gob.mx/group/ and each
    one aggregates datasets published by one or more government institutions.
    """

    slug: str = Field(description="URL-safe identifier used in paths, e.g. 'seguridad'.")
    name: str = Field(description="Human-readable display name, e.g. 'Seguridad'.")
    description: Optional[str] = Field(
        default=None,
        description="Short summary of what the category covers, as shown on the listing page.",
    )
    dataset_count: int = Field(
        description="Number of datasets currently associated with this category."
    )
    image_url: Optional[str] = Field(
        default=None,
        description="Absolute URL of the category's SVG icon.",
    )
    url: str = Field(description="Absolute URL to the category's dataset listing page.")


class CategoriesResponse(BaseModel):
    """Wrapper returned by the REST server's GET /categories endpoint."""

    total: int = Field(description="Total number of categories returned.")
    categories: list[Category] = Field(description="List of category objects.")


class Dataset(BaseModel):
    """A single dataset (base de datos) listed under a category page.

    Each dataset is published by a government institution and may contain
    one or more individual resource files (CSV, etc.). The ``resource_count``
    field reflects the number of those files, not the number of rows.
    """

    slug: str = Field(
        description="URL-safe identifier, e.g. 'incidencia_delictiva'. "
                    "Matches the last path segment of the dataset URL."
    )
    title: str = Field(description="Full display title of the dataset.")
    last_updated: Optional[str] = Field(
        default=None,
        description="Date of the last update as a Spanish-locale string, "
                    "e.g. '3 de marzo 2026'. Not parsed into a date object.",
    )
    description: Optional[str] = Field(
        default=None,
        description="Short description extracted from the listing card. "
                    "May be truncated if the site shows an ellipsis.",
    )
    category_slug: Optional[str] = Field(
        default=None,
        description="Slug of the category this dataset belongs to, e.g. 'seguridad'.",
    )
    category_name: Optional[str] = Field(
        default=None,
        description="Display name of the category, e.g. 'Seguridad'.",
    )
    organization_slug: Optional[str] = Field(
        default=None,
        description="Slug of the publishing institution, e.g. 'sesnsp'.",
    )
    organization_name: Optional[str] = Field(
        default=None,
        description="Full name of the publishing institution.",
    )
    resource_count: Optional[int] = Field(
        default=None,
        description="Number of resource files (CSV, etc.) attached to this dataset.",
    )
    url: str = Field(description="Absolute URL to the dataset's detail page.")


class DatasetsResponse(BaseModel):
    """Wrapper returned by the REST server's GET /categories/{slug}/datasets endpoint."""

    total: int = Field(description="Total number of datasets returned.")
    category_slug: str = Field(description="The category slug that was queried.")
    datasets: list[Dataset] = Field(description="List of dataset objects.")
