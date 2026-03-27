# Gobierno

> **135 datasets** · Source: [datos.gob.mx/group/gobierno](https://www.datos.gob.mx/group/gobierno)

## Description

Contiene datos relacionados con la administración pública y políticas gubernamentales, incluyendo transparencia, rendición de cuentas y gestión pública.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 135 |
| Source URL | https://www.datos.gob.mx/group/gobierno |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("gobierno")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/gobierno/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/gobierno)
