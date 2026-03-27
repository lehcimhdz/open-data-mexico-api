from pydantic import BaseModel
from typing import Optional

class Category(BaseModel):
    slug: str
    name: str
    description: Optional[str] = None
    dataset_count: int
    image_url: Optional[str] = None
    url: str

class CategoriesResponse(BaseModel):
    total: int
    categories: list[Category]

class Dataset(BaseModel):
    slug: str
    title: str
    last_updated: Optional[str] = None
    description: Optional[str] = None
    category_slug: Optional[str] = None
    category_name: Optional[str] = None
    organization_slug: Optional[str] = None
    organization_name: Optional[str] = None
    resource_count: Optional[int] = None
    url: str

class DatasetsResponse(BaseModel):
    total: int
    category_slug: str
    datasets: list[Dataset]
