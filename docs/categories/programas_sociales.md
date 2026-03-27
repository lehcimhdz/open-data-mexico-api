# Programas sociales

> **153 datasets** · Source: [datos.gob.mx/group/programas_sociales](https://www.datos.gob.mx/group/programas_sociales)

## Description

Datos sobre las iniciativas y acciones implementadas por el gobierno federal para mejorar el bienestar y reducir las desigualdades sociales.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 153 |
| Source URL | https://www.datos.gob.mx/group/programas_sociales |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("programas_sociales")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/programas_sociales/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/programas_sociales)
