# Agricultura

> **139 datasets** · Source: [datos.gob.mx/group/agricultura](https://www.datos.gob.mx/group/agricultura)

## Description

Datos sobre la actividad agrícola, ganadera, pesquera y de cultivos: su producción, volúmenes, precios, rendimientos y superficie sembrada y cosechada.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 139 |
| Source URL | https://www.datos.gob.mx/group/agricultura |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("agricultura")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/agricultura/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/agricultura)
