# open-data-mexico

Unofficial async Python client for [datos.gob.mx](https://www.datos.gob.mx/) — the Mexican government's open data platform, built on CKAN 2.11.

---

## Installation

```bash
pip install open-data-mexico
```

The **PyPI package name** is `open-data-mexico` (hyphen).
The **Python import name** is `open_data_mexico` (underscore).

```python
from open_data_mexico import DatosGobMX   # ← always use underscore
```

Requires Python 3.11+. No API key needed.

---

## Quick Start

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:

        # Search by keyword
        results = await client.search("incidencia delictiva")
        print(f"{results.total} datasets found")

        # Browse a category
        datasets = await client.get_category_datasets("seguridad")
        print(f"{len(datasets)} datasets in 'seguridad'")

        # Full detail + resources
        detail = await client.get_dataset("incidencia_delictiva")
        for r in detail.resources:
            print(f"  [{r.format}] {r.name}")

asyncio.run(main())
```

---

## Client parameters

```python
async with DatosGobMX(
    timeout=30.0,         # HTTP timeout in seconds
    request_delay=0.5,    # sleep between requests (polite rate limiting)
    max_retries=3,        # retry on 5xx / 429 with exponential backoff
    cache_ttl=300.0,      # in-memory cache TTL in seconds (0 = disabled)
) as client:
    ...
```

---

## Methods at a glance

| Method | Returns | Description |
|--------|---------|-------------|
| `get_categories()` | `list[Category]` | All 28 thematic categories |
| `get_category(slug)` | `Category \| None` | Single category by slug |
| `get_category_datasets(slug)` | `list[Dataset]` | All datasets in a category |
| `get_dataset(slug)` | `DatasetDetail \| None` | Full dataset with resources |
| `get_resource_data(resource)` | `str` | Download CSV into memory |
| `search(query, *, category, limit, offset)` | `SearchResponse` | Full-text keyword search |
| `get_organizations()` | `list[Organization]` | All 184+ publishing institutions |
| `get_organization(slug)` | `Organization \| None` | Single institution by slug |

---

## Search

Search across all datasets using the CKAN `package_search` API:

```python
async with DatosGobMX() as client:
    # Basic search
    results = await client.search("rezago social")
    print(f"{results.total} results")
    for ds in results.datasets:
        print(f"  {ds.slug}: {ds.title} ({ds.organization_name})")

    # Filter by category + paginate
    page = await client.search("salud", category="salud", limit=10, offset=20)
    print(f"Showing {len(page.datasets)} of {page.total}")
```

`SearchResponse` fields: `total`, `query`, `category`, `offset`, `datasets`.

---

## Categories

Browse the 28 thematic categories. Each category page in this documentation lists its notable datasets and example code.

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

Dataset counts reflect the site as of March 2026 and change over time.

```python
async with DatosGobMX() as client:
    categories = await client.get_categories()
    for cat in categories:
        print(f"{cat.slug}: {cat.name} ({cat.dataset_count} datasets)")
        # cat.url  → "https://www.datos.gob.mx/group/{slug}"
```

---

## Datasets and resources

```python
async with DatosGobMX() as client:
    # List datasets in a category (auto-paginates)
    datasets = await client.get_category_datasets("seguridad")
    for ds in datasets:
        # ds.last_updated is a timezone-aware datetime (UTC)
        print(f"{ds.last_updated:%Y-%m-%d}  {ds.title}")

    # Full detail
    detail = await client.get_dataset("incidencia_delictiva")
    print(detail.license_name)   # "Creative Commons Attribution 4.0"
    print(detail.tags)           # ["Feminicidio", "Homicidio doloso", ...]

    # Download a resource CSV into memory (no disk writes)
    import io, pandas as pd
    csv_str = await client.get_resource_data(detail.resources[0])
    df = pd.read_csv(io.StringIO(csv_str))
    print(df.shape)
```

All datetime fields (`last_updated`, `created`) are **timezone-aware UTC `datetime` objects**, compatible with pandas, JSON serialization via Pydantic, and direct arithmetic.

---

## Organizations

```python
async with DatosGobMX() as client:
    orgs = await client.get_organizations()
    print(f"{len(orgs)} organizations")

    coneval = await client.get_organization("coneval")
    # coneval.slug           → "coneval"
    # coneval.title          → "Consejo Nacional de Evaluación... (CONEVAL)"
    # coneval.dataset_count  → 2
    # coneval.created        → datetime(2015, 3, 1, tzinfo=UTC)
```

---

## FastAPI server (optional)

```bash
pip install "open-data-mexico[server]"
uvicorn server.app:app --reload
# Docs at http://localhost:8000/docs
```

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/categories` | All categories |
| `GET` | `/categories/{slug}` | Single category |
| `GET` | `/categories/{slug}/datasets` | Datasets in a category |
| `GET` | `/datasets/{slug}` | Full dataset detail |
| `GET` | `/organizations` | All organizations |
| `GET` | `/organizations/{slug}` | Single organization |
| `GET` | `/search?q=...` | Full-text search (params: `category`, `limit`, `offset`) |

---

## Serialize to JSON

All models are Pydantic v2. `datetime` fields serialize as ISO 8601 strings:

```python
detail = await client.get_dataset("incidencia_delictiva")

# As a dict
d = detail.model_dump()

# As a JSON string (datetimes → "2026-03-03T22:09:46Z")
print(detail.model_dump_json(indent=2))
```

---

## Data source

All data is fetched live from [datos.gob.mx](https://www.datos.gob.mx/) using a combination of HTML scraping (BeautifulSoup4 + lxml) and the public CKAN JSON API (`/api/3/action/...`). No local database, no credentials.
