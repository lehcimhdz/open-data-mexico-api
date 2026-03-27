# Cultura

> **187 datasets** · Source: [datos.gob.mx/group/cultura](https://www.datos.gob.mx/group/cultura)

## Description

Información sobre el patrimonio cultural, eventos artísticos, tradicionales y culturales, así como sobre las instituciones e infraestructura cultural del país.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 187 |
| Source URL | https://www.datos.gob.mx/group/cultura |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("cultura")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/cultura/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/cultura)
