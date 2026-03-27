# Derechos humanos

> **53 datasets** · Source: [datos.gob.mx/group/derechos_humanos](https://www.datos.gob.mx/group/derechos_humanos)

## Description

Datos relacionados con la protección y promoción de los derechos de las personas, incluyendo registros de violaciones y mecanismos de atención.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 53 |
| Source URL | https://www.datos.gob.mx/group/derechos_humanos |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("derechos_humanos")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/derechos_humanos/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/derechos_humanos)
