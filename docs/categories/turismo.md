# Turismo

> **5 datasets** · Source: [datos.gob.mx/group/turismo](https://www.datos.gob.mx/group/turismo)

## Description

Datos sobre la actividad turística en el país, su desarrollo e impacto económico, incluyendo flujos de visitantes e infraestructura turística.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 5 |
| Source URL | https://www.datos.gob.mx/group/turismo |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("turismo")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/turismo/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/turismo)
