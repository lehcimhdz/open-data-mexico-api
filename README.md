# Open Data Mexico API

An **unofficial** REST API that scrapes [datos.gob.mx](https://www.datos.gob.mx/) — the Mexican government's open data portal (CKAN 2.11.2) — and exposes the data as a structured JSON API.

> **Disclaimer:** This is an unofficial project with no affiliation with the Mexican government or CKAN. It scrapes public HTML pages. Use responsibly and respect the site's terms of service. The API may break if the site's HTML structure changes.

---

## Available Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Root — API info and link to docs |
| `GET` | `/categories` | List all dataset categories |
| `GET` | `/categories/{slug}` | Get a single category by slug |
| `GET` | `/docs` | Interactive Swagger UI documentation |
| `GET` | `/redoc` | ReDoc documentation |

### Example responses

**GET /categories**
```json
{
  "total": 28,
  "categories": [
    {
      "slug": "agricultura",
      "name": "Agricultura",
      "description": "Datos sobre la actividad agricola...",
      "dataset_count": 139,
      "image_url": "https://www.datos.gob.mx/uploads/group/agricultura.svg",
      "url": "https://www.datos.gob.mx/group/agricultura"
    }
  ]
}
```

**GET /categories/agricultura**
```json
{
  "slug": "agricultura",
  "name": "Agricultura",
  "description": "Datos sobre la actividad agricola...",
  "dataset_count": 139,
  "image_url": "https://www.datos.gob.mx/uploads/group/agricultura.svg",
  "url": "https://www.datos.gob.mx/group/agricultura"
}
```

---

## Installation

```bash
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive documentation.

## Running Tests

```bash
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

---

## Project Structure

```
open-data-mexico-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and route definitions
│   ├── config.py        # Base URL and HTTP headers
│   ├── scrapers/
│   │   ├── __init__.py
│   │   └── categories.py  # HTML scraper for /group/ pages
│   └── models/
│       ├── __init__.py
│       └── schemas.py     # Pydantic models
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Pytest fixtures with mock HTML
│   └── test_categories.py # Unit and integration tests
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Tech Stack

- **FastAPI** — web framework
- **httpx** — async HTTP client for scraping
- **BeautifulSoup4 + lxml** — HTML parsing
- **Pydantic** — data validation and serialization
- **pytest + pytest-asyncio + pytest-httpx** — testing
