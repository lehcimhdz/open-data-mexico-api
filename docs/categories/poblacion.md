# Población

> **138 datasets** · Source: [datos.gob.mx/group/poblacion](https://www.datos.gob.mx/group/poblacion)

## Description

Datos referentes a la composición demográfica del país, natalidad, mortalidad, distribución territorial y proyecciones de población.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 138 |
| Source URL | https://www.datos.gob.mx/group/poblacion |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("poblacion")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/poblacion/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/poblacion)
