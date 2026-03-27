# Ciencia y tecnología

> **194 datasets** · Source: [datos.gob.mx/group/ciencia_tecnologia](https://www.datos.gob.mx/group/ciencia_tecnologia)

## Description

Bases de datos relacionadas con proyectos de investigación científica, desarrollo tecnológico e innovación financiados o promovidos por el gobierno.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 194 |
| Source URL | https://www.datos.gob.mx/group/ciencia_tecnologia |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("ciencia_tecnologia")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/ciencia_tecnologia/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/ciencia_tecnologia)
