from fastapi import FastAPI, HTTPException
from app.models.schemas import Category, CategoriesResponse
from app.scrapers.categories import fetch_all_categories

app = FastAPI(
    title="Open Data Mexico API",
    description="Unofficial API for datos.gob.mx — scrapes CKAN HTML to expose structured data.",
    version="1.0.0",
)


@app.get("/", summary="Root", description="API root with links to documentation.")
async def root():
    return {"message": "Open Data Mexico API", "docs": "/docs"}


@app.get(
    "/categories",
    response_model=CategoriesResponse,
    summary="List all categories",
    description="Returns all dataset categories available on datos.gob.mx.",
)
async def get_categories():
    categories = await fetch_all_categories()
    return CategoriesResponse(total=len(categories), categories=categories)


@app.get(
    "/categories/{slug}",
    response_model=Category,
    summary="Get category by slug",
    description="Returns a single category by its slug identifier. Returns 404 if not found.",
)
async def get_category(slug: str):
    categories = await fetch_all_categories()
    for category in categories:
        if category.slug == slug:
            return category
    raise HTTPException(status_code=404, detail=f"Category '{slug}' not found.")
