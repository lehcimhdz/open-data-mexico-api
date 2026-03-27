# Plan de Apertura de Datos

> **140 datasets** · Source: [datos.gob.mx/group/plan_apertura_datos](https://www.datos.gob.mx/group/plan_apertura_datos)

## Description

Esta categoría concentra el Plan Institucional de Publicación de Datos de las dependencias y entidades de la Administración Pública Federal.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 140 |
| Source URL | https://www.datos.gob.mx/group/plan_apertura_datos |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("plan_apertura_datos")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/plan_apertura_datos/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/plan_apertura_datos)
