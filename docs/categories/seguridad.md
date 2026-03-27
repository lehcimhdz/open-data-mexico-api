# Seguridad

> **403 datasets** · Format: CSV · License: Creative Commons Attribution 4.0 (CC-BY-4.0)
> Source: [datos.gob.mx/group/seguridad](https://www.datos.gob.mx/group/seguridad)

## Description

Datos a nivel federal y estatal sobre los delitos presuntamente cometidos, registros de investigaciones y estadísticas sobre criminalidad.

## At a glance

| Stat | Value |
|------|-------|
| Total datasets | 403 |
| File format | CSV |
| License | Creative Commons Attribution 4.0 (CC-BY-4.0) |
| Contributing institutions | 8 |
| Source URL | https://www.datos.gob.mx/group/seguridad |

## Contributing institutions

| Institution | Slug | Datasets |
|-------------|------|----------|
| Prevención y Reinserción Social (PRS) | `prs` | 364 |
| Servicio de Protección Federal (SPF) | `spf` | 20 |
| Comisión Ejecutiva de Atención a Víctimas (CEAV) | `ceav` | 8 |
| Secretaría de Marina (SEMAR) | `secretaria_marina` | 4 |
| Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública (SESNSP) | `sesnsp` | 3 |
| Agencia Reguladora del Transporte Ferroviario (ARTF) | `artf` | 2 |
| Comisión Nacional de Acuacultura y Pesca (CONAPESCA) | `conapesca` | 1 |
| Servicio Nacional de Sanidad, Inocuidad y Calidad Agroalimentaria (SENASICA) | `senasica` | 1 |

## Notable datasets

| Dataset | Slug | Institution | Resources | Last Updated |
|---------|------|-------------|-----------|--------------|
| Incidencia delictiva | `incidencia_delictiva` | SESNSP | 3 | 3 de marzo 2026 |
| Expedientes Clasificados CEAV | `expedientes_clasificados_ceav` | CEAV | 1 | 23 de marzo 2026 |
| Inscripción en el Registro Nacional de Víctimas (RENAVI) | `inscripcion_registro_nacional_victimas_renavi` | CEAV | 1 | 23 de marzo 2026 |
| Cuaderno Mensual Estadístico Penitenciario (enero, 2026) | `cuaderno_mensual_estadistico_penitenciario_enero_2026` | PRS | 52 | 10 de marzo 2026 |
| Bajas de personal | `bajas_personal` | SEMAR | 2 | 12 de febrero 2026 |
| Estadísticas del personal naval | `estadisticas_del_personal_naval` | SEMAR | 2 | 12 de febrero 2026 |
| Reportes de seguridad en el Sistema Ferroviario Mexicano | `reportes_seguridad_sistema_ferroviario` | ARTF | 2 | 9 de enero 2026 |
| Certificaciones en estándares de competencia | `certificaciones_estandares_competencia` | SPF | 10 | 29 de diciembre 2025 |
| Programa de formación Inicial de Guardias y Policías del SPF | `formacion_inicial_guardias_policias` | SPF | 10 | 29 de diciembre 2025 |
| Registro Federal de Víctimas (REFEVI) | `registro_federal_victimas_refevi` | CEAV | 3 | 8 de octubre 2025 |

## Usage

### Python

#### Fetch all datasets in Seguridad

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("seguridad")
        print(f"Found {len(datasets)} datasets")
        for ds in datasets:
            print(f"  {ds.title} ({ds.organization_name})")

asyncio.run(main())
```

#### Filter by institution (PRS has 364 of the 403 datasets)

```python
import asyncio
from open_data_mexico import DatosGobMX

async def prs_datasets():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("seguridad")
        prs = [ds for ds in datasets if ds.organization_slug == "prs"]
        print(f"PRS datasets: {len(prs)}")
        for ds in prs:
            print(f"  {ds.title} — {ds.resource_count} archivos")

asyncio.run(prs_datasets())
```

#### Get the category metadata

```python
import asyncio
from open_data_mexico import DatosGobMX

async def category_info():
    async with DatosGobMX() as client:
        cat = await client.get_category("seguridad")
        print(cat.model_dump())

asyncio.run(category_info())
```

#### Find the most recently updated datasets

```python
import asyncio
from open_data_mexico import DatosGobMX

async def recent():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("seguridad")
        # datasets are ordered by most recently updated (site default)
        for ds in datasets[:5]:
            print(f"{ds.last_updated}: {ds.title}")

asyncio.run(recent())
```

### REST API

```bash
# Category metadata
curl http://localhost:8000/categories/seguridad

# All datasets (returns DatasetsResponse JSON)
curl http://localhost:8000/categories/seguridad/datasets
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/seguridad)
