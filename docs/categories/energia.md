# Energía

> **271 datasets** · Source: [datos.gob.mx/group/energia](https://www.datos.gob.mx/group/energia)

## Description

Datos sobre la producción y distribución de energía, hidrocarburos y energías renovables, así como infraestructura energética nacional.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 271 |
| Source URL | https://www.datos.gob.mx/group/energia |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("energia")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/energia/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/energia)
