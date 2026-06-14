"""Optional FastAPI REST server exposing the open-data-mexico client."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware

from open_data_mexico import (
    CategoriesResponse,
    Category,
    DatasetDetail,
    DatasetsResponse,
    DatosGobMX,
    Organization,
    OrganizationsResponse,
    SearchResponse,
    __version__,
)


def _allowed_origins() -> list[str]:
    """Read the CORS allow-list from ``CORS_ORIGINS`` (comma-separated)."""
    raw = os.environ.get("CORS_ORIGINS", "*").strip()
    if raw == "*":
        return ["*"]
    return [o.strip() for o in raw.split(",") if o.strip()]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create a single shared DatosGobMX client for the lifetime of the server.

    Using one client means:
    - A single persistent httpx.AsyncClient (connection pool reuse).
    - A shared in-memory TTL cache across all requests.
    """
    async with DatosGobMX() as client:
        app.state.client = client
        yield


def _get_client(request: Request) -> DatosGobMX:
    """Return the shared client from app state.

    Falls back to a per-request client when the lifespan has not run
    (e.g., during testing with ASGITransport without lifespan support).
    """
    return getattr(request.app.state, "client", None) or DatosGobMX()


app = FastAPI(
    title="Open Data Mexico API",
    description="Unofficial REST API for datos.gob.mx",
    version=__version__,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins(),
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/", tags=["meta"])
async def root():
    return {"message": "Open Data Mexico API", "docs": "/docs", "version": __version__}


@app.get("/health", tags=["meta"])
async def health():
    """Lightweight liveness probe — does not touch the upstream site."""
    return {"status": "ok", "version": __version__}


@app.get("/categories", response_model=CategoriesResponse, tags=["categories"])
async def list_categories(request: Request):
    categories = await _get_client(request).get_categories()
    return CategoriesResponse(total=len(categories), categories=categories)


@app.get("/categories/{slug}", response_model=Category, tags=["categories"])
async def get_category(slug: str, request: Request):
    category = await _get_client(request).get_category(slug)
    if category is None:
        raise HTTPException(status_code=404, detail=f"Category '{slug}' not found")
    return category


@app.get(
    "/categories/{slug}/datasets",
    response_model=DatasetsResponse,
    tags=["categories"],
)
async def list_category_datasets(slug: str, request: Request):
    client = _get_client(request)
    category = await client.get_category(slug)
    if category is None:
        raise HTTPException(status_code=404, detail=f"Category '{slug}' not found")
    datasets = await client.get_category_datasets(slug)
    return DatasetsResponse(total=len(datasets), category_slug=slug, datasets=datasets)


@app.get("/datasets/{slug}", response_model=DatasetDetail, tags=["datasets"])
async def get_dataset(slug: str, request: Request):
    detail = await _get_client(request).get_dataset(slug)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Dataset '{slug}' not found")
    return detail


@app.get(
    "/organizations",
    response_model=OrganizationsResponse,
    tags=["organizations"],
)
async def list_organizations(request: Request):
    """List all government organizations that publish datasets."""
    orgs = await _get_client(request).get_organizations()
    return OrganizationsResponse(total=len(orgs), organizations=orgs)


@app.get(
    "/organizations/{slug}",
    response_model=Organization,
    tags=["organizations"],
)
async def get_organization(slug: str, request: Request):
    """Fetch a single organization by slug."""
    org = await _get_client(request).get_organization(slug)
    if org is None:
        raise HTTPException(status_code=404, detail=f"Organization '{slug}' not found")
    return org


@app.get("/search", response_model=SearchResponse, tags=["search"])
async def search_datasets(
    request: Request,
    q: str = Query(..., description="Free-text search term, e.g. 'rezago social'"),
    category: str | None = Query(None, description="Category slug to restrict results"),
    limit: int = Query(20, ge=1, le=1000, description="Results per page"),
    offset: int = Query(0, ge=0, description="Results to skip for pagination"),
):
    """Search datasets by keyword across all categories."""
    return await _get_client(request).search(q, category=category, limit=limit, offset=offset)
