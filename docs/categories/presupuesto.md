# Presupuesto

> **313 datasets** · Source: [datos.gob.mx/group/presupuesto](https://www.datos.gob.mx/group/presupuesto)

## Description

Bases de datos relacionados con la asignación, distribución y ejecución del gasto público federal, incluyendo el Presupuesto de Egresos de la Federación.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 313 |
| Source URL | https://www.datos.gob.mx/group/presupuesto |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("presupuesto")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/presupuesto/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/presupuesto)
