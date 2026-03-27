# Deporte

> **10 datasets** · Source: [datos.gob.mx/group/deporte](https://www.datos.gob.mx/group/deporte)

## Description

Información sobre la práctica deportiva en el país, el fomento de la actividad física, infraestructura deportiva y resultados de competencias.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 10 |
| Source URL | https://www.datos.gob.mx/group/deporte |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("deporte")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/deporte/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/deporte)
