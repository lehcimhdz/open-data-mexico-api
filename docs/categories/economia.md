# Economía

> **284 datasets** · Source: [datos.gob.mx/group/economia](https://www.datos.gob.mx/group/economia)

## Description

Bases de datos sobre inversión pública y privada, desarrollo económico, comercio exterior, indicadores financieros y actividad empresarial.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 284 |
| Source URL | https://www.datos.gob.mx/group/economia |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("economia")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/economia/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/economia)
