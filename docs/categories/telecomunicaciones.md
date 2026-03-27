# Telecomunicaciones

> **73 datasets** · Source: [datos.gob.mx/group/telecomunicaciones](https://www.datos.gob.mx/group/telecomunicaciones)

## Description

Datos sobre los servicios de telefonía, internet, televisión y radio en el país, incluyendo cobertura, tarifas e infraestructura.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 73 |
| Source URL | https://www.datos.gob.mx/group/telecomunicaciones |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("telecomunicaciones")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/telecomunicaciones/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/telecomunicaciones)
