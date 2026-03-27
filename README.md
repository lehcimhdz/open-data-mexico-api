# open-data-mexico

![PyPI version](https://img.shields.io/pypi/v/open-data-mexico)

Unofficial Python client for [datos.gob.mx](https://www.datos.gob.mx/) — the Mexican government's open data platform (CKAN).

> **Disclaimer:** This is an unofficial project with no affiliation with the Mexican government or CKAN. It scrapes public HTML pages. Use responsibly and respect the site's terms of service. The client may break if the site's HTML structure changes.

---

## Installation

```bash
pip install open-data-mexico
```

## Quick Start

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        # Fetch all categories
        categories = await client.get_categories()
        for cat in categories:
            print(f"{cat.slug}: {cat.name} ({cat.dataset_count} datasets)")

        # Fetch a single category by slug
        salud = await client.get_category("salud")
        if salud:
            print(salud.model_dump())

asyncio.run(main())
```

---

## Available Methods

| Method | Return type | Description |
|--------|-------------|-------------|
| `get_categories()` | `list[Category]` | Fetch all categories from datos.gob.mx/group/ |
| `get_category(slug)` | `Category \| None` | Fetch a single category by slug; returns None if not found |

### Category model fields

| Field | Type | Description |
|-------|------|-------------|
| `slug` | `str` | URL identifier |
| `name` | `str` | Human-readable name |
| `description` | `str \| None` | Short description |
| `dataset_count` | `int` | Number of datasets in the category |
| `image_url` | `str \| None` | Category image URL |
| `url` | `str` | Full URL to the category page |

---

## Optional: FastAPI Server

Install the server extra to run a REST API on top of the library:

```bash
pip install open-data-mexico[server]
```

Run the server:

```bash
uvicorn server.app:app --reload
```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive Swagger documentation.

### Server endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Root — API info |
| `GET` | `/categories` | List all dataset categories |
| `GET` | `/categories/{slug}` | Get a single category by slug |
| `GET` | `/docs` | Interactive Swagger UI |
| `GET` | `/redoc` | ReDoc documentation |

---

## Development Setup

```bash
pip install open-data-mexico[dev]
pytest
```

Or with verbose output:

```bash
pytest -v
```

---

## Available Categories (28)

The portal currently exposes 28 thematic categories:

| Slug | Name |
|------|------|
| `agricultura` | Agricultura |
| `catalogo_datos` | Catalogo de Datos |
| `ciencia_tecnologia` | Ciencia y Tecnologia |
| `cultura` | Cultura |
| `deporte` | Deporte |
| `derechos_humanos` | Derechos Humanos |
| `economia` | Economia |
| `educacion` | Educacion |
| `energia` | Energia |
| `gobierno` | Gobierno |
| `infraestructura` | Infraestructura |
| `mar_costa` | Mar y Costa |
| `medio_ambiente` | Medio Ambiente |
| `migracion` | Migracion |
| `movilidad` | Movilidad |
| `mujeres` | Mujeres |
| `multiculturalidad` | Multiculturalidad |
| `plan_apertura_datos` | Plan de Apertura de Datos |
| `poblacion` | Poblacion |
| `presupuesto` | Presupuesto |
| `programas_sociales` | Programas Sociales |
| `salud` | Salud |
| `seguridad` | Seguridad |
| `servicios` | Servicios |
| `telecomunicaciones` | Telecomunicaciones |
| `territorio` | Territorio |
| `trabajo` | Trabajo |
| `turismo` | Turismo |
