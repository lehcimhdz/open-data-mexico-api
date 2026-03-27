# Servicios

> **189 datasets** · Source: [datos.gob.mx/group/servicios](https://www.datos.gob.mx/group/servicios)

## Description

Bases de datos relacionadas con las acciones que la Administración Pública Federal realiza para proveer servicios a la ciudadanía.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 189 |
| Source URL | https://www.datos.gob.mx/group/servicios |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("servicios")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/servicios/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/servicios)
