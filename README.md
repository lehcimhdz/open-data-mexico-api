# open-data-mexico

![PyPI version](https://img.shields.io/pypi/v/open-data-mexico)
![Python](https://img.shields.io/pypi/pyversions/open-data-mexico)
![License](https://img.shields.io/pypi/l/open-data-mexico)

Unofficial Python client for [datos.gob.mx](https://www.datos.gob.mx/) — the Mexican government's open data platform, built on CKAN 2.11.

> **Disclaimer:** This is an unofficial project with no affiliation with the Mexican government or CKAN. It scrapes public HTML pages and may break if the site's structure changes. Use responsibly and respect the site's terms of service.

---

## Installation

```bash
pip install open-data-mexico
```

Requires Python 3.11+.

---

## Quick Start

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        # List all 28 categories
        categories = await client.get_categories()
        for cat in categories:
            print(f"{cat.slug}: {cat.name} ({cat.dataset_count} datasets)")

        # Get a single category by slug
        salud = await client.get_category("salud")
        print(salud.name, salud.dataset_count)

        # List all datasets in a category (auto-paginates)
        datasets = await client.get_category_datasets("seguridad")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name} ({ds.last_updated})")

asyncio.run(main())
```

---

## Client Reference

### `DatosGobMX(...)`

Async context-manager client. A shared HTTP connection is reused across
all method calls when used as a context manager, which is more efficient
for multiple consecutive requests.

```python
# Recommended — reuses one HTTP connection
async with DatosGobMX() as client:
    categories = await client.get_categories()

# Also valid — opens a new connection per call
client = DatosGobMX()
categories = await client.get_categories()

# With rate limiting (0.5s between requests)
async with DatosGobMX(request_delay=0.5) as client:
    datasets = await client.get_category_datasets("educacion")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `timeout` | `float` | `30.0` | HTTP request timeout in seconds |
| `request_delay` | `float` | `0.0` | Seconds to wait between requests (rate limiting) |
| `max_retries` | `int` | `3` | Retry attempts on 5xx/429 or network errors |
| `cache_ttl` | `float` | `300.0` | Seconds to cache responses in memory (0 = disabled) |

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_categories()` | `list[Category]` | All 28 categories (auto-paginates) |
| `get_category(slug)` | `Category \| None` | One category by slug; `None` if not found |
| `get_category_datasets(category_slug)` | `list[Dataset]` | All datasets in a category (auto-paginates) |
| `get_dataset(slug)` | `DatasetDetail \| None` | Full dataset detail page including resources |
| `get_resource_data(resource)` | `str` | CSV content in-memory, no disk writes |

All methods raise `httpx.HTTPStatusError` on non-2xx responses and
`httpx.RequestError` on network failures (timeout, DNS, etc.).

---

## Data Models

### `Category`

Represents a thematic category grouping datasets.

| Field | Type | Description |
|-------|------|-------------|
| `slug` | `str` | URL identifier, e.g. `"seguridad"` |
| `name` | `str` | Display name, e.g. `"Seguridad"` |
| `description` | `str \| None` | Short summary shown on the listing page |
| `dataset_count` | `int` | Number of datasets in this category |
| `image_url` | `str \| None` | Absolute URL of the category's SVG icon |
| `url` | `str` | Absolute URL to the category's dataset listing |

### `Dataset`

Represents a single dataset listed under a category page.

| Field | Type | Description |
|-------|------|-------------|
| `slug` | `str` | URL identifier, e.g. `"incidencia_delictiva"` |
| `title` | `str` | Full display title |
| `last_updated` | `str \| None` | Last update as a Spanish-locale string, e.g. `"3 de marzo 2026"` |
| `description` | `str \| None` | Short description from the listing card (may be truncated) |
| `category_slug` | `str \| None` | Slug of the parent category |
| `category_name` | `str \| None` | Display name of the parent category |
| `organization_slug` | `str \| None` | Slug of the publishing institution |
| `organization_name` | `str \| None` | Full name of the publishing institution |
| `resource_count` | `int \| None` | Number of resource files (CSV, etc.) attached |
| `url` | `str` | Absolute URL to the dataset's detail page |

### `Resource`

Represents a single downloadable resource file attached to a dataset.

| Field | Type | Description |
|-------|------|-------------|
| `resource_id` | `str` | UUID of the resource, from the `li[data-id]` attribute |
| `name` | `str` | Display name of the resource file |
| `description` | `str \| None` | Short description of this resource file's contents |
| `format` | `str \| None` | File format in lowercase, e.g. `"csv"`, `"xlsx"` |
| `category_slug` | `str \| None` | Slug of the category this resource belongs to |
| `category_name` | `str \| None` | Display name of the category |
| `organization_slug` | `str \| None` | Slug of the publishing institution |
| `organization_name` | `str \| None` | Full name of the publishing institution |
| `download_url` | `str \| None` | Direct URL to download the raw file |
| `detail_url` | `str \| None` | Absolute URL to the resource's detail page on datos.gob.mx |

### `DatasetDetail`

Full detail of a dataset page at `datos.gob.mx/dataset/{slug}`.

| Field | Type | Description |
|-------|------|-------------|
| `slug` | `str` | URL identifier of the dataset |
| `title` | `str` | Full display title |
| `description` | `str \| None` | Full description of what the dataset contains |
| `organization_slug` | `str \| None` | Slug of the publishing institution |
| `organization_name` | `str \| None` | Full name of the publishing institution |
| `license_name` | `str \| None` | License display name, e.g. `"Creative Commons Attribution 4.0"` |
| `license_url` | `str \| None` | URL to the license text |
| `tags` | `list[str]` | List of tag strings associated with this dataset |
| `created` | `str \| None` | ISO 8601 creation datetime, e.g. `"2026-03-23T16:28:17+0000"` |
| `last_updated` | `str \| None` | ISO 8601 last-updated datetime |
| `resources` | `list[Resource]` | List of downloadable resource files |
| `url` | `str` | Absolute URL to this dataset's page |

---

## Working with Dataset Data

### Fetching dataset details

```python
async with DatosGobMX() as client:
    detail = await client.get_dataset("expedientes_clasificados_ceav")
    print(detail.title)           # "Expedientes Clasificados CEAV"
    print(detail.organization_name)  # "Comisión Ejecutiva de Atención a Víctimas (CEAV)"
    print(detail.license_name)    # "Creative Commons Attribution 4.0"
    print(detail.tags)            # ["transparencia", "expediente", ...]

    for resource in detail.resources:
        print(resource.name, resource.format, resource.download_url)
```

### Loading CSV data into memory (no disk writes)

`get_resource_data()` downloads the CSV file and returns it as a Python string.
The data **never touches disk** — it lives entirely in memory.

**With pandas:**
```python
import io
import pandas as pd

async with DatosGobMX() as client:
    detail = await client.get_dataset("expedientes_clasificados_ceav")
    resource = detail.resources[0]

    csv_str = await client.get_resource_data(resource)
    df = pd.read_csv(io.StringIO(csv_str))
    print(df.head())
    print(df.dtypes)
```

Install pandas: `pip install open-data-mexico[pandas]`

**With the built-in `csv` module (no extra dependencies):**
```python
import io
import csv

async with DatosGobMX() as client:
    detail = await client.get_dataset("expedientes_clasificados_ceav")
    resource = detail.resources[0]

    csv_str = await client.get_resource_data(resource)
    reader = csv.DictReader(io.StringIO(csv_str))
    rows = list(reader)
    print(rows[0])  # {'col1': 'val1', ...}
```

**As JSON-serializable dicts:**
```python
import io, csv, json

csv_str = await client.get_resource_data(resource)
rows = list(csv.DictReader(io.StringIO(csv_str)))
print(json.dumps(rows[:3], ensure_ascii=False, indent=2))
```

> **Note on encoding:** Mexican government CSV files sometimes use latin-1 encoding.
> `get_resource_data()` automatically falls back to latin-1 if UTF-8 decoding fails.

---

## Optional: FastAPI Server

Install with the `server` extra to run a REST API on top of the library:

```bash
pip install open-data-mexico[server]
```

Start the server:

```bash
uvicorn server.app:app --reload
```

The API is available at `http://localhost:8000`. Interactive docs at `/docs` (Swagger UI) and `/redoc`.

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | API info and version |
| `GET` | `/categories` | All categories → `CategoriesResponse` |
| `GET` | `/categories/{slug}` | Single category → `Category` (404 if not found) |
| `GET` | `/categories/{slug}/datasets` | All datasets in a category → `DatasetsResponse` |
| `GET` | `/datasets/{slug}` | Full dataset detail → `DatasetDetail` |

Example responses:

```jsonc
// GET /categories/seguridad
{
  "slug": "seguridad",
  "name": "Seguridad",
  "description": "Datos a nivel federal y estatal sobre los delitos...",
  "dataset_count": 403,
  "image_url": "https://www.datos.gob.mx/uploads/group/...seguridad.svg",
  "url": "https://www.datos.gob.mx/group/seguridad"
}

// GET /categories/seguridad/datasets  (abbreviated)
{
  "total": 403,
  "category_slug": "seguridad",
  "datasets": [
    {
      "slug": "incidencia_delictiva",
      "title": "Incidencia delictiva",
      "last_updated": "3 de marzo 2026",
      "description": "Se muestran los hechos delictivos...",
      "category_slug": "seguridad",
      "category_name": "Seguridad",
      "organization_slug": "sesnsp",
      "organization_name": "Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública (SESNSP)",
      "resource_count": 3,
      "url": "https://www.datos.gob.mx/dataset/incidencia_delictiva"
    }
  ]
}
```

---

## Development

```bash
# Clone and install all dev dependencies
pip install -e ".[dev]"

# Run the full test suite (with coverage)
pytest

# Without coverage (faster)
pytest --no-cov -v

# Lint
ruff check .

# Type check
mypy open_data_mexico/
```

### Project layout

```
open_data_mexico/          # installable library package
├── __init__.py            # public API surface
├── _config.py             # BASE_URL and HTTP headers (private)
├── client.py              # DatosGobMX async client class
├── models.py              # Pydantic data models
└── _scrapers/             # HTML scraping internals (private)
    ├── categories.py      # scraper for /group/ listing pages
    ├── datasets.py        # scraper for /group/{slug} dataset pages
    └── dataset_detail.py  # scraper for /dataset/{slug} detail pages
server/
└── app.py                 # optional FastAPI REST server
tests/
├── conftest.py            # shared mock HTML fixtures
├── test_categories.py     # 10 tests
├── test_datasets.py       # 8 tests
└── test_dataset_detail.py # 26 tests
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
| `educacion` | Educación | 1420 |
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
