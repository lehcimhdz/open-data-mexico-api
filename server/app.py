from fastapi import FastAPI, HTTPException
from open_data_mexico import DatosGobMX, Category, CategoriesResponse, Dataset, DatasetsResponse, DatasetDetail

app = FastAPI(
    title="Open Data Mexico API",
    description="Unofficial REST API for datos.gob.mx",
    version="0.1.0",
)

@app.get("/")
async def root():
    return {"message": "Open Data Mexico API", "docs": "/docs", "version": "0.1.0"}

@app.get("/categories", response_model=CategoriesResponse)
async def list_categories():
    async with DatosGobMX() as client:
        categories = await client.get_categories()
    return CategoriesResponse(total=len(categories), categories=categories)

@app.get("/categories/{slug}", response_model=Category)
async def get_category(slug: str):
    async with DatosGobMX() as client:
        category = await client.get_category(slug)
    if category is None:
        raise HTTPException(status_code=404, detail=f"Category '{slug}' not found")
    return category

@app.get("/categories/{slug}/datasets", response_model=DatasetsResponse)
async def list_category_datasets(slug: str):
    async with DatosGobMX() as client:
        # First verify category exists
        category = await client.get_category(slug)
        if category is None:
            raise HTTPException(status_code=404, detail=f"Category '{slug}' not found")
        datasets = await client.get_category_datasets(slug)
    return DatasetsResponse(total=len(datasets), category_slug=slug, datasets=datasets)


@app.get("/datasets/{slug}", response_model=DatasetDetail)
async def get_dataset(slug: str):
    """Fetch full detail for a dataset by slug."""
    async with DatosGobMX() as client:
        detail = await client.get_dataset(slug)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Dataset '{slug}' not found")
    return detail
