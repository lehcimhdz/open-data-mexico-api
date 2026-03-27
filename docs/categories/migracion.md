# Migración

> **48 datasets** · Source: [datos.gob.mx/group/migracion](https://www.datos.gob.mx/group/migracion)

## Description

Datos sobre los flujos de movilidad de las personas a nivel nacional e internacional, incluyendo migración interna, emigración e inmigración.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 48 |
| Source URL | https://www.datos.gob.mx/group/migracion |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("migracion")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/migracion/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/migracion)
