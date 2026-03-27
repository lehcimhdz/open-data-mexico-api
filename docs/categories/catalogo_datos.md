# Catálogo de datos

> **5 datasets** · Source: [datos.gob.mx/group/catalogo_datos](https://www.datos.gob.mx/group/catalogo_datos)

## Description

Categoría que contiene catálogos de datos que en conjunto con los demás conjuntos de datos del portal, permiten el enriquecimiento de los datos.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 5 |
| Source URL | https://www.datos.gob.mx/group/catalogo_datos |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("catalogo_datos")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/catalogo_datos/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/catalogo_datos)
