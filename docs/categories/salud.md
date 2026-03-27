# Salud

> **573 datasets** · Source: [datos.gob.mx/group/salud](https://www.datos.gob.mx/group/salud)

## Description

Incluye datos relacionados con el bienestar físico y mental de la población, servicios de salud, enfermedades y mortalidad.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 573 |
| Source URL | https://www.datos.gob.mx/group/salud |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("salud")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/salud/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/salud)
