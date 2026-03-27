# open-data-mexico — Documentation

[datos.gob.mx](https://www.datos.gob.mx/) is the Mexican government's official open data portal, built on CKAN 2.11. It publishes thousands of datasets across 28 thematic categories, contributed by federal and state institutions covering topics from public health and education to security, environment, and the economy.

This documentation section covers how to use the `open-data-mexico` Python library to access each of those 28 categories programmatically.

---

## Categories

| Slug | Name | Datasets | Docs |
|------|------|----------|------|
| `agricultura` | Agricultura | 139 | [agricultura.md](./categories/agricultura.md) |
| `catalogo_datos` | Catálogo de datos | 5 | [catalogo_datos.md](./categories/catalogo_datos.md) |
| `ciencia_tecnologia` | Ciencia y tecnología | 194 | [ciencia_tecnologia.md](./categories/ciencia_tecnologia.md) |
| `cultura` | Cultura | 187 | [cultura.md](./categories/cultura.md) |
| `deporte` | Deporte | 10 | [deporte.md](./categories/deporte.md) |
| `derechos_humanos` | Derechos humanos | 53 | [derechos_humanos.md](./categories/derechos_humanos.md) |
| `economia` | Economía | 284 | [economia.md](./categories/economia.md) |
| `educacion` | Educación | 1420 | [educacion.md](./categories/educacion.md) |
| `energia` | Energía | 271 | [energia.md](./categories/energia.md) |
| `gobierno` | Gobierno | 135 | [gobierno.md](./categories/gobierno.md) |
| `infraestructura` | Infraestructura | 125 | [infraestructura.md](./categories/infraestructura.md) |
| `mar_costa` | Mar y costa | 588 | [mar_costa.md](./categories/mar_costa.md) |
| `medio_ambiente` | Medio ambiente | 205 | [medio_ambiente.md](./categories/medio_ambiente.md) |
| `migracion` | Migración | 48 | [migracion.md](./categories/migracion.md) |
| `movilidad` | Movilidad | 41 | [movilidad.md](./categories/movilidad.md) |
| `mujeres` | Mujeres | 23 | [mujeres.md](./categories/mujeres.md) |
| `multiculturalidad` | Multiculturalidad | 8 | [multiculturalidad.md](./categories/multiculturalidad.md) |
| `plan_apertura_datos` | Plan de Apertura de Datos | 140 | [plan_apertura_datos.md](./categories/plan_apertura_datos.md) |
| `poblacion` | Población | 138 | [poblacion.md](./categories/poblacion.md) |
| `presupuesto` | Presupuesto | 313 | [presupuesto.md](./categories/presupuesto.md) |
| `programas_sociales` | Programas sociales | 153 | [programas_sociales.md](./categories/programas_sociales.md) |
| `salud` | Salud | 573 | [salud.md](./categories/salud.md) |
| `seguridad` | Seguridad | 403 | [seguridad.md](./categories/seguridad.md) |
| `servicios` | Servicios | 189 | [servicios.md](./categories/servicios.md) |
| `telecomunicaciones` | Telecomunicaciones | 73 | [telecomunicaciones.md](./categories/telecomunicaciones.md) |
| `territorio` | Territorio | 121 | [territorio.md](./categories/territorio.md) |
| `trabajo` | Trabajo | 239 | [trabajo.md](./categories/trabajo.md) |
| `turismo` | Turismo | 5 | [turismo.md](./categories/turismo.md) |

Dataset counts reflect the site as of March 2026 and will change over time.

---

## How to use

The `get_categories()` method returns all 28 categories in a single call, auto-paginating as needed.

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        categories = await client.get_categories()
        for cat in categories:
            print(f"{cat.slug}: {cat.name} ({cat.dataset_count} datasets)")
            print(f"  {cat.url}")

asyncio.run(main())
```

Each `Category` object exposes: `slug`, `name`, `description`, `dataset_count`, `image_url`, and `url`. See the per-category pages linked above for dataset-level usage examples.
