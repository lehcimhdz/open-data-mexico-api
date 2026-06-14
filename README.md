# open-data-mexico

![PyPI version](https://img.shields.io/pypi/v/open-data-mexico)
![Python](https://img.shields.io/pypi/pyversions/open-data-mexico)
![License](https://img.shields.io/pypi/l/open-data-mexico)
![CI](https://github.com/lehcimhdz/open-data-mexico-api/actions/workflows/ci.yml/badge.svg)
[![Coverage](https://codecov.io/gh/lehcimhdz/open-data-mexico-api/branch/main/graph/badge.svg)](https://codecov.io/gh/lehcimhdz/open-data-mexico-api)

Unofficial async Python client for [datos.gob.mx](https://www.datos.gob.mx/) — the Mexican government's open data platform, built on CKAN 2.11. Browse 28 thematic categories, search across 5 000+ datasets, fetch metadata, and download CSV data directly into memory.

> **Disclaimer:** This is an unofficial project with no affiliation with the Mexican government or CKAN. It scrapes public HTML pages and calls the public CKAN JSON API; it may break if the site's structure changes. Use responsibly and respect the site's terms of service.

---

## Installation

```bash
pip install open-data-mexico
```

Requires **Python 3.11+**. No API key needed.

### Optional extras

```bash
# Include pandas for loading CSVs into DataFrames
pip install "open-data-mexico[pandas]"

# Include the optional FastAPI REST server
pip install "open-data-mexico[server]"

# Both
pip install "open-data-mexico[pandas,server]"
```

---

## Quick Start

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:

        # Search datasets by keyword
        results = await client.search("incidencia delictiva")
        print(f"{results.total} datasets found")
        for ds in results.datasets:
            print(f"  {ds.title} — {ds.organization_name}")

        # Browse a category
        datasets = await client.get_category_datasets("seguridad")
        print(f"\n{len(datasets)} datasets in 'seguridad'")

        # Get full detail + resources for a dataset
        detail = await client.get_dataset("incidencia_delictiva")
        print(f"\n{detail.title}")
        for r in detail.resources:
            print(f"  [{r.format}] {r.name}")

asyncio.run(main())
```

---

## Package name vs. import name

| Context | Value |
|---------|-------|
| **Install from PyPI** | `pip install open-data-mexico` |
| **Import in Python** | `from open_data_mexico import DatosGobMX` |

The package uses a hyphen (`open-data-mexico`) on PyPI; the Python module uses an underscore (`open_data_mexico`) as required by Python's import system.

---

## Client Reference

### `DatosGobMX(...)`

Async context manager. One persistent `httpx.AsyncClient` is reused across all calls when entering the context, which gives you connection-pool reuse and a shared in-memory cache.

```python
# Recommended — single connection, shared cache
async with DatosGobMX() as client:
    categories = await client.get_categories()

# Also valid — opens a new connection for each call
client = DatosGobMX()
categories = await client.get_categories()

# With polite rate limiting (0.5 s between requests)
async with DatosGobMX(request_delay=0.5) as client:
    datasets = await client.get_category_datasets("educacion")
```

**Constructor parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `timeout` | `float` | `30.0` | HTTP request timeout in seconds |
| `request_delay` | `float` | `0.0` | Seconds to sleep between requests (polite rate limiting) |
| `max_retries` | `int` | `3` | Retry attempts on 5xx / 429 or transient network errors (exponential backoff: 2 s, 4 s, 8 s) |
| `cache_ttl` | `float` | `300.0` | Seconds to cache responses in memory; `0` disables caching |
| `concurrency` | `int` | `5` | Max number of pages fetched in parallel during auto-pagination |

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_categories()` | `list[Category]` | All 28 thematic categories (auto-paginates, parallel) |
| `get_category(slug)` | `Category \| None` | Single category by slug; `None` if not found |
| `get_category_datasets(slug)` | `list[Dataset]` | All datasets in a category (auto-paginates all pages in parallel) |
| `iter_category_datasets(slug)` | `AsyncIterator[Dataset]` | Streaming variant — yields page-by-page, bypasses the cache |
| `get_dataset(slug)` | `DatasetDetail \| None` | Full dataset detail including all resources; `None` if not found |
| `get_resource_data(resource)` | `str` | Download raw file content (CSV) into a string — UTF-8 with latin-1 fallback |
| `get_resource_bytes(resource)` | `bytes` | Download raw bytes — use for XLSX/ZIP/SHP/PDF |
| `get_resource_dataframe(resource, **kw)` | `pandas.DataFrame` | One-line CSV/XLSX → DataFrame (requires `[pandas]` extra) |
| `search(query, *, category, limit, offset)` | `SearchResponse` | Full-text search across all datasets via CKAN API |
| `get_organizations()` | `list[Organization]` | All 184+ publishing institutions (auto-paginates) |
| `get_organization(slug)` | `Organization \| None` | Single organization by slug; `None` if not found |
| `clear_cache()` | `None` | Drop every entry from the in-memory response cache |
| `invalidate(key_prefix)` | `int` | Drop cache entries whose key starts with the prefix; returns count |

All methods raise `httpx.HTTPStatusError` on unrecoverable HTTP errors and `httpx.RequestError` on network failures (timeout, DNS, etc.). Transient 5xx / 429 errors are retried automatically up to `max_retries` times.

---

## Data Models

All models are [Pydantic v2](https://docs.pydantic.dev/latest/) — they serialize cleanly to/from JSON with `.model_dump()` and `.model_dump_json()`.

### `Category`

| Field | Type | Example |
|-------|------|---------|
| `slug` | `str` | `"seguridad"` |
| `name` | `str` | `"Seguridad"` |
| `description` | `str \| None` | `"Datos sobre criminalidad..."` |
| `dataset_count` | `int` | `403` |
| `image_url` | `str \| None` | `"https://www.datos.gob.mx/uploads/group/seguridad.svg"` |
| `url` | `str` | `"https://www.datos.gob.mx/group/seguridad"` |

### `Dataset`

Returned by `get_category_datasets()` and `search()`.

| Field | Type | Example |
|-------|------|---------|
| `slug` | `str` | `"incidencia_delictiva"` |
| `title` | `str` | `"Incidencia delictiva"` |
| `last_updated` | `datetime \| None` | `datetime(2026, 3, 3, tzinfo=UTC)` |
| `description` | `str \| None` | Short card excerpt (may be truncated) |
| `category_slug` | `str \| None` | `"seguridad"` |
| `category_name` | `str \| None` | `"Seguridad"` |
| `organization_slug` | `str \| None` | `"sesnsp"` |
| `organization_name` | `str \| None` | `"Secretariado Ejecutivo del SNSP (SESNSP)"` |
| `resource_count` | `int \| None` | `3` |
| `url` | `str` | `"https://www.datos.gob.mx/dataset/incidencia_delictiva"` |

### `DatasetDetail`

Returned by `get_dataset()`. Extends `Dataset` with full metadata and resources.

| Field | Type | Example |
|-------|------|---------|
| `slug` | `str` | `"incidencia_delictiva"` |
| `title` | `str` | `"Incidencia delictiva"` |
| `description` | `str \| None` | Full description of the dataset |
| `organization_slug` | `str \| None` | `"sesnsp"` |
| `organization_name` | `str \| None` | Full institution name |
| `license_name` | `str \| None` | `"Creative Commons Attribution 4.0"` |
| `license_url` | `str \| None` | `"https://creativecommons.org/licenses/by/4.0/"` |
| `tags` | `list[str]` | `["Feminicidio", "Homicidio doloso", ...]` |
| `created` | `datetime \| None` | `datetime(2025, 3, 13, 23, 27, 31, tzinfo=UTC)` |
| `last_updated` | `datetime \| None` | `datetime(2026, 3, 3, 22, 9, 46, tzinfo=UTC)` |
| `resources` | `list[Resource]` | Downloadable files attached to this dataset |
| `url` | `str` | `"https://www.datos.gob.mx/dataset/incidencia_delictiva"` |

### `Resource`

| Field | Type | Example |
|-------|------|---------|
| `resource_id` | `str` | `"d9b2792a-33a2-4ea8-8527-210d9e99de5e"` |
| `name` | `str` | `"Incidencia Delictiva Nacional Estatal"` |
| `description` | `str \| None` | Description of this file's contents |
| `format` | `str \| None` | `"csv"` |
| `category_slug` | `str \| None` | `"seguridad"` |
| `category_name` | `str \| None` | `"Seguridad"` |
| `organization_slug` | `str \| None` | `"sesnsp"` |
| `organization_name` | `str \| None` | Full institution name |
| `download_url` | `str \| None` | Direct URL to the raw file |
| `detail_url` | `str \| None` | URL to the resource's detail page |

### `Organization`

Returned by `get_organizations()` and `get_organization()`.

| Field | Type | Example |
|-------|------|---------|
| `slug` | `str` | `"coneval"` |
| `title` | `str` | `"Consejo Nacional de Evaluación... (CONEVAL)"` |
| `description` | `str \| None` | Short description of the institution |
| `dataset_count` | `int` | `2` |
| `image_url` | `str \| None` | Logo URL |
| `created` | `datetime \| None` | `datetime(2015, 3, 1, tzinfo=UTC)` |
| `url` | `str` | `"https://www.datos.gob.mx/organization/coneval"` |

### `SearchResponse`

Returned by `search()`.

| Field | Type | Description |
|-------|------|-------------|
| `total` | `int` | Total matching datasets (may exceed `len(datasets)` if paginated) |
| `query` | `str` | The search term used |
| `category` | `str \| None` | Category filter applied, if any |
| `offset` | `int` | Number of results skipped |
| `datasets` | `list[Dataset]` | Results for this page |

---

## Usage Examples

### Search datasets by keyword

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        # Basic search
        results = await client.search("rezago social")
        print(f"{results.total} results for '{results.query}'")
        for ds in results.datasets:
            print(f"  {ds.slug}: {ds.title}")

        # Search within a category with pagination
        page2 = await client.search("educacion", category="educacion", limit=10, offset=10)
        print(f"\nPage 2 — showing {len(page2.datasets)} of {page2.total}")

asyncio.run(main())
```

### Browse a category and filter results

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("seguridad")

        # Filter by institution
        sesnsp = [ds for ds in datasets if ds.organization_slug == "sesnsp"]
        print(f"SESNSP datasets: {len(sesnsp)}")

        # Most recently updated
        for ds in datasets[:5]:
            print(f"{ds.last_updated:%Y-%m-%d}  {ds.title}")

asyncio.run(main())
```

### Get full dataset detail and resources

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        detail = await client.get_dataset("incidencia_delictiva")
        if detail is None:
            print("Not found")
            return

        print(detail.title)
        print(f"License: {detail.license_name}")
        print(f"Tags: {', '.join(detail.tags)}")
        print(f"Updated: {detail.last_updated:%Y-%m-%d}")

        for r in detail.resources:
            print(f"  [{r.format}] {r.name}")
            print(f"    {r.download_url}")

asyncio.run(main())
```

### Load CSV data into pandas (no disk writes)

```python
import asyncio
import io
import pandas as pd
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        detail = await client.get_dataset("incidencia_delictiva")
        resource = detail.resources[0]

        csv_str = await client.get_resource_data(resource)
        df = pd.read_csv(io.StringIO(csv_str))
        print(df.shape)
        print(df.head())

asyncio.run(main())
```

> **Encoding note:** Some government CSV files use Latin-1 encoding. `get_resource_data()` automatically falls back to Latin-1 if UTF-8 decoding fails.

### One-line CSV → DataFrame (with `[pandas]` extra)

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        detail = await client.get_dataset("incidencia_delictiva")
        df = await client.get_resource_dataframe(detail.resources[0])
        print(df.shape)

asyncio.run(main())
```

`get_resource_dataframe()` dispatches on `resource.format`: `csv`/`txt` use `pandas.read_csv` (UTF-8 with latin-1 fallback), `xls`/`xlsx` use `pandas.read_excel`. Pass any keyword arguments through to the underlying reader (`sep="\t"`, `nrows=100`, `sheet_name="Hoja2"`…).

### Download binary resources (XLSX, ZIP, SHP, PDF…)

```python
data: bytes = await client.get_resource_bytes(resource)
```

### Stream a large category page-by-page

```python
async with DatosGobMX() as client:
    async for ds in client.iter_category_datasets("educacion"):
        if "primaria" in ds.title.lower():
            print(ds.slug)
            break  # stops fetching further pages immediately
```

### Cache management

```python
client.invalidate("datasets:seguridad")  # drop one category's listing
client.clear_cache()                      # drop everything
```

### List and look up organizations

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        # All 184+ institutions
        orgs = await client.get_organizations()
        print(f"{len(orgs)} organizations")
        for org in orgs[:5]:
            print(f"  {org.slug}: {org.title} ({org.dataset_count} datasets)")

        # Single lookup
        coneval = await client.get_organization("coneval")
        if coneval:
            print(coneval.description)

asyncio.run(main())
```

### Serialize to JSON

```python
import asyncio, json
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        results = await client.search("pobreza")
        # Pydantic v2 — datetime fields serialize as ISO 8601 strings
        print(results.model_dump_json(indent=2))

asyncio.run(main())
```

---

## Command-line interface

Installing the package also installs the `open-data-mx` console script:

```bash
open-data-mx categories                          # list all 28 categories
open-data-mx category seguridad                  # show one category
open-data-mx datasets seguridad --limit 5        # first 5 datasets in seguridad
open-data-mx dataset incidencia_delictiva        # full detail + resources
open-data-mx organizations                       # 184+ institutions
open-data-mx organization coneval
open-data-mx search "rezago social" --limit 3    # full-text search
open-data-mx search educacion --category educacion --limit 10 --offset 10
open-data-mx download incidencia_delictiva --output ./data --format csv
```

Global flags:

| Flag | Default | Description |
|------|---------|-------------|
| `--json` | off | Emit machine-readable JSON instead of human-readable text |
| `--timeout SEC` | 30 | HTTP timeout |
| `--delay SEC` | 0 | Polite delay between requests |
| `--retries N` | 3 | Retry attempts on 5xx/429 |
| `--concurrency N` | 5 | Max parallel page fetches |

The `--json` flag is handy for piping into `jq`:

```bash
open-data-mx --json categories | jq '.[] | select(.dataset_count > 200) | .slug'
```

---

## Optional: FastAPI REST Server

Install with the `server` extra to expose the library as a local REST API:

```bash
pip install "open-data-mexico[server]"
uvicorn server.app:app --reload
```

Interactive docs at `http://localhost:8000/docs` (Swagger UI) and `/redoc`.

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | API info and version |
| `GET` | `/health` | Liveness probe — `{"status": "ok", "version": "..."}` |
| `GET` | `/categories` | All 28 categories → `CategoriesResponse` |
| `GET` | `/categories/{slug}` | Single category → `Category` (404 if not found) |
| `GET` | `/categories/{slug}/datasets` | All datasets in a category → `DatasetsResponse` |
| `GET` | `/datasets/{slug}` | Full dataset detail → `DatasetDetail` (404 if not found) |
| `GET` | `/organizations` | All organizations → `OrganizationsResponse` |
| `GET` | `/organizations/{slug}` | Single organization → `Organization` (404 if not found) |
| `GET` | `/search?q=...` | Full-text search → `SearchResponse` |

CORS is enabled by default for all origins. Tighten it with the `CORS_ORIGINS` environment variable (comma-separated):

```bash
CORS_ORIGINS="https://app.example.com,https://staging.example.com" uvicorn server.app:app
```

**Search query parameters:**

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `q` | yes | — | Free-text search term |
| `category` | no | — | Category slug to restrict results |
| `limit` | no | `20` | Results per page (max 1000) |
| `offset` | no | `0` | Results to skip for pagination |

**Example requests:**

```bash
# Search
curl "http://localhost:8000/search?q=rezago+social"
curl "http://localhost:8000/search?q=educacion&category=educacion&limit=5&offset=10"

# Categories
curl http://localhost:8000/categories/seguridad
curl http://localhost:8000/categories/seguridad/datasets

# Dataset detail
curl http://localhost:8000/datasets/incidencia_delictiva

# Organizations
curl http://localhost:8000/organizations
curl http://localhost:8000/organizations/coneval
```

**Example response — `GET /search?q=rezago+social`:**

```json
{
  "total": 12,
  "query": "rezago social",
  "category": null,
  "offset": 0,
  "datasets": [
    {
      "slug": "rezago_social",
      "title": "Rezago social",
      "last_updated": "2025-06-04T18:44:31Z",
      "description": "Medida que permite ordenar unidades geográficas...",
      "category_slug": "poblacion",
      "category_name": "Población",
      "organization_slug": "coneval",
      "organization_name": "Consejo Nacional de Evaluación... (CONEVAL)",
      "resource_count": 17,
      "url": "https://www.datos.gob.mx/dataset/rezago_social"
    }
  ]
}
```

---

## Development

```bash
# Clone and install all dev dependencies
git clone https://github.com/lehcimhdz/open-data-mexico-api.git
cd open-data-mexico-api
pip install -e ".[dev]"

# Run the full test suite (with coverage report)
pytest

# Faster run without coverage
pytest --no-cov -v

# Lint + format
ruff check .
ruff format .

# Type check
mypy open_data_mexico/
```

### Project layout

```
open_data_mexico/             # installable library package
├── __init__.py               # public API surface
├── _config.py                # BASE_URL, headers, defaults (private)
├── _http.py                  # robust_get() with retry/backoff (private)
├── _utils.py                 # datetime parsing helpers (private)
├── client.py                 # DatosGobMX async client
├── models.py                 # Pydantic data models
├── py.typed                  # PEP 561 marker
└── _scrapers/                # scraping internals (private)
    ├── categories.py         # /group/ listing pages
    ├── datasets.py           # /group/{slug} dataset pages
    ├── dataset_detail.py     # /dataset/{slug} detail pages
    ├── organizations.py      # CKAN organization_list / organization_show
    └── search.py             # CKAN package_search
server/
└── app.py                    # optional FastAPI REST server
tests/
├── conftest.py               # shared HTML fixtures
├── test_categories.py
├── test_datasets.py
├── test_dataset_detail.py
├── test_organizations.py
└── test_search.py
```

---

## Available Categories (28)

Dataset counts reflect the site as of March 2026 and will change over time.

| Slug | Name | Datasets |
|------|------|----------|
| `agricultura` | Agricultura | 139 |
| `catalogo_datos` | Catálogo de datos | 5 |
| `ciencia_tecnologia` | Ciencia y tecnología | 194 |
| `cultura` | Cultura | 187 |
| `deporte` | Deporte | 10 |
| `derechos_humanos` | Derechos humanos | 53 |
| `economia` | Economía | 284 |
| `educacion` | Educación | 1 420 |
| `energia` | Energía | 271 |
| `gobierno` | Gobierno | 135 |
| `infraestructura` | Infraestructura | 125 |
| `mar_costa` | Mar y costa | 588 |
| `medio_ambiente` | Medio ambiente | 205 |
| `migracion` | Migración | 48 |
| `movilidad` | Movilidad | 41 |
| `mujeres` | Mujeres | 23 |
| `multiculturalidad` | Multiculturalidad | 8 |
| `plan_apertura_datos` | Plan de Apertura de Datos | 140 |
| `poblacion` | Población | 138 |
| `presupuesto` | Presupuesto | 313 |
| `programas_sociales` | Programas sociales | 153 |
| `salud` | Salud | 573 |
| `seguridad` | Seguridad | 403 |
| `servicios` | Servicios | 189 |
| `telecomunicaciones` | Telecomunicaciones | 73 |
| `territorio` | Territorio | 121 |
| `trabajo` | Trabajo | 239 |
| `turismo` | Turismo | 5 |
