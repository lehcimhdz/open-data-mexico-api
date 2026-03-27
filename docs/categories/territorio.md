# Territorio

> **121 datasets** · Source: [datos.gob.mx/group/territorio](https://www.datos.gob.mx/group/territorio)

## Description

Bases de datos relacionados con el espacio geográfico en sus diferentes dimensiones: física, política, administrativa y catastral.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 121 |
| Source URL | https://www.datos.gob.mx/group/territorio |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("territorio")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/territorio/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/territorio)
