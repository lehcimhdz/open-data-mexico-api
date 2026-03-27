# Mujeres

> **23 datasets** · Source: [datos.gob.mx/group/mujeres](https://www.datos.gob.mx/group/mujeres)

## Description

Datos con perspectiva de género. Integra conjuntos de datos sobre la situación de las mujeres en distintos ámbitos: económico, social, educativo y de salud.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 23 |
| Source URL | https://www.datos.gob.mx/group/mujeres |

## Usage

### Python

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("mujeres")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} — {ds.organization_name}")

asyncio.run(main())
```

### REST API

```bash
curl http://localhost:8000/categories/mujeres/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/mujeres)
