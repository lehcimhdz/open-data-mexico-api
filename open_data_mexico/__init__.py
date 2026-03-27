"""
open-data-mexico: Unofficial Python client for datos.gob.mx
"""
from open_data_mexico.client import DatosGobMX
from open_data_mexico.models import Category, CategoriesResponse

__version__ = "0.1.0"
__all__ = ["DatosGobMX", "Category", "CategoriesResponse"]
