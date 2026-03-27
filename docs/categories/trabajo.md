# Trabajo

> **239 datasets** · Source: [datos.gob.mx/group/trabajo](https://www.datos.gob.mx/group/trabajo)

## Description

Datos sobre el mercado laboral, empleo, desempleo, salarios, condiciones de trabajo y relaciones laborales en México.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 239 |
| Source URL | https://www.datos.gob.mx/group/trabajo |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("trabajo")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/trabajo/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/trabajo)
