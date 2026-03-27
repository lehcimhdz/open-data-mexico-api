from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request

from open_data_mexico import DatosGobMX, Category, CategoriesResponse, DatasetsResponse, DatasetDetail


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
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Open Data Mexico API", "docs": "/docs", "version": "0.1.0"}


@app.get("/categories", response_model=CategoriesResponse)
async def list_categories(request: Request):
    categories = await _get_client(request).get_categories()
    return CategoriesResponse(total=len(categories), categories=categories)


@app.get("/categories/{slug}", response_model=Category)
async def get_category(slug: str, request: Request):
    category = await _get_client(request).get_category(slug)
    if category is None:
        raise HTTPException(status_code=404, detail=f"Category '{slug}' not found")
    return category


@app.get("/categories/{slug}/datasets", response_model=DatasetsResponse)
async def list_category_datasets(slug: str, request: Request):
    client = _get_client(request)
    category = await client.get_category(slug)
    if category is None:
        raise HTTPException(status_code=404, detail=f"Category '{slug}' not found")
    datasets = await client.get_category_datasets(slug)
    return DatasetsResponse(total=len(datasets), category_slug=slug, datasets=datasets)


@app.get("/datasets/{slug}", response_model=DatasetDetail)
async def get_dataset(slug: str, request: Request):
    detail = await _get_client(request).get_dataset(slug)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Dataset '{slug}' not found")
    return detail
