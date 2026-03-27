# Educación

> **1420 datasets** · Source: [datos.gob.mx/group/educacion](https://www.datos.gob.mx/group/educacion)

## Description

Abarca datos sobre la cobertura, calidad y acceso a los servicios educativos en todos los niveles, desde educación básica hasta superior.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 1420 |
| Source URL | https://www.datos.gob.mx/group/educacion |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("educacion")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/educacion/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/educacion)
