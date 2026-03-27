# Infraestructura

> **125 datasets** · Source: [datos.gob.mx/group/infraestructura](https://www.datos.gob.mx/group/infraestructura)

## Description

Datos relacionados con el desarrollo, mantenimiento y gestión de los sistemas de infraestructura pública del país.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 125 |
| Source URL | https://www.datos.gob.mx/group/infraestructura |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("infraestructura")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/infraestructura/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/infraestructura)
