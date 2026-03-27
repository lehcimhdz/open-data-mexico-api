"""
Pydantic models representing data scraped from datos.gob.mx.

All models are read-only data containers. Field values are extracted
from the site's public HTML pages and reflect whatever the site
currently publishes — no transformations beyond basic text cleanup.
"""

from pydantic import BaseModel, Field


class Category(BaseModel):
    """A thematic category grouping datasets on datos.gob.mx.

    Categories are listed at https://www.datos.gob.mx/group/ and each
    one aggregates datasets published by one or more government institutions.
    """

    slug: str = Field(description="URL-safe identifier used in paths, e.g. 'seguridad'.")
    name: str = Field(description="Human-readable display name, e.g. 'Seguridad'.")
    description: str | None = Field(
        default=None,
        description="Short summary of what the category covers, as shown on the listing page.",
    )
    dataset_count: int = Field(
        description="Number of datasets currently associated with this category."
    )
    image_url: str | None = Field(
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
    last_updated: str | None = Field(
        default=None,
        description="Date of the last update as a Spanish-locale string, "
        "e.g. '3 de marzo 2026'. Not parsed into a date object.",
    )
    description: str | None = Field(
        default=None,
        description="Short description extracted from the listing card. "
        "May be truncated if the site shows an ellipsis.",
    )
    category_slug: str | None = Field(
        default=None,
        description="Slug of the category this dataset belongs to, e.g. 'seguridad'.",
    )
    category_name: str | None = Field(
        default=None,
        description="Display name of the category, e.g. 'Seguridad'.",
    )
    organization_slug: str | None = Field(
        default=None,
        description="Slug of the publishing institution, e.g. 'sesnsp'.",
    )
    organization_name: str | None = Field(
        default=None,
        description="Full name of the publishing institution.",
    )
    resource_count: int | None = Field(
        default=None,
        description="Number of resource files (CSV, etc.) attached to this dataset.",
    )
    url: str = Field(description="Absolute URL to the dataset's detail page.")


class DatasetsResponse(BaseModel):
    """Wrapper returned by the REST server's GET /categories/{slug}/datasets endpoint."""

    total: int = Field(description="Total number of datasets returned.")
    category_slug: str = Field(description="The category slug that was queried.")
    datasets: list[Dataset] = Field(description="List of dataset objects.")


class Resource(BaseModel):
    """A single downloadable resource file attached to a dataset.

    Each resource is a concrete file (CSV, XLSX, etc.) published as part
    of a dataset. The ``download_url`` points directly to the file and can
    be streamed in-memory without writing to disk.
    """

    resource_id: str = Field(description="UUID of the resource, from the li[data-id] attribute.")
    name: str = Field(description="Display name of the resource file.")
    description: str | None = Field(
        default=None, description="Short description of this resource file's contents."
    )
    format: str | None = Field(
        default=None, description="File format in lowercase, e.g. 'csv', 'xlsx'."
    )
    category_slug: str | None = Field(
        default=None, description="Slug of the category this resource belongs to."
    )
    category_name: str | None = Field(default=None, description="Display name of the category.")
    organization_slug: str | None = Field(
        default=None, description="Slug of the publishing institution."
    )
    organization_name: str | None = Field(
        default=None, description="Full name of the publishing institution."
    )
    download_url: str | None = Field(
        default=None,
        description="Direct URL to download the raw file (e.g. a CSV on repodatos.atdt.gob.mx). "
        "Use client.get_resource_data() to stream this into memory without saving to disk.",
    )
    detail_url: str | None = Field(
        default=None, description="Absolute URL to the resource's detail page on datos.gob.mx."
    )


class DatasetDetail(BaseModel):
    """Full detail of a dataset page at datos.gob.mx/dataset/{slug}.

    A dataset groups one or more Resource files published by a government
    institution. Use client.get_resource_data(resource) to load any CSV
    resource directly into memory as a string, then parse with pandas or
    the csv module.
    """

    slug: str = Field(description="URL identifier of the dataset.")
    title: str = Field(description="Full display title.")
    description: str | None = Field(
        default=None, description="Full description of what the dataset contains."
    )
    organization_slug: str | None = Field(
        default=None, description="Slug of the publishing institution."
    )
    organization_name: str | None = Field(
        default=None, description="Full name of the publishing institution."
    )
    license_name: str | None = Field(
        default=None, description="License display name, e.g. 'Creative Commons Attribution 4.0'."
    )
    license_url: str | None = Field(default=None, description="URL to the license text.")
    tags: list[str] = Field(
        default_factory=list, description="List of tag strings associated with this dataset."
    )
    created: str | None = Field(
        default=None,
        description="ISO 8601 creation datetime from data-datetime attr, e.g. '2026-03-23T16:28:17+0000'.",  # noqa: E501
    )
    last_updated: str | None = Field(
        default=None, description="ISO 8601 last-updated datetime from data-datetime attr."
    )
    resources: list[Resource] = Field(
        default_factory=list, description="List of downloadable resource files."
    )
    url: str = Field(description="Absolute URL to this dataset's page.")
