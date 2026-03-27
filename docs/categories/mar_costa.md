# Mar y costa

> **588 datasets** · Source: [datos.gob.mx/group/mar_costa](https://www.datos.gob.mx/group/mar_costa)

## Description

Información relacionada con la investigación, monitoreo, administración y aprovechamiento sustentable de los mares, costas y recursos marinos de México.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 588 |
| Source URL | https://www.datos.gob.mx/group/mar_costa |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("mar_costa")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/mar_costa/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/mar_costa)
