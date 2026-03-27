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
