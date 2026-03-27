# Movilidad

> **41 datasets** · Source: [datos.gob.mx/group/movilidad](https://www.datos.gob.mx/group/movilidad)

## Description

Información sobre los sistemas de transporte, accesibilidad y desplazamiento de personas y mercancías en el territorio nacional.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 41 |
| Source URL | https://www.datos.gob.mx/group/movilidad |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("movilidad")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/movilidad/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/movilidad)
