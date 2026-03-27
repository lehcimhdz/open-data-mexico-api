from fastapi import FastAPI, HTTPException
from open_data_mexico import DatosGobMX, Category, CategoriesResponse

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
