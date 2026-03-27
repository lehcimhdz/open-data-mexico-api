# Medio ambiente

> **205 datasets** · Source: [datos.gob.mx/group/medio_ambiente](https://www.datos.gob.mx/group/medio_ambiente)

## Description

Información sobre actividades de cuidado, protección, conservación, y aprovechamiento sustentable de los recursos naturales y el medio ambiente.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 205 |
| Source URL | https://www.datos.gob.mx/group/medio_ambiente |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("medio_ambiente")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/medio_ambiente/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/medio_ambiente)
