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
| Secretariado Ejecutivo del SNSP (SESNSP) | `sesnsp` | 3 |
| Agencia Reguladora del Transporte Ferroviario (ARTF) | `artf` | 2 |
| Comisión Nacional de Acuacultura y Pesca (CONAPESCA) | `conapesca` | 1 |
| SENASICA | `senasica` | 1 |

## Notable datasets

| Dataset | Slug | Institution | Resources |
|---------|------|-------------|-----------|
| Incidencia delictiva | `incidencia_delictiva` | SESNSP | 3 |
| Expedientes Clasificados CEAV | `expedientes_clasificados_ceav` | CEAV | 1 |
| Inscripción en el RENAVI | `inscripcion_registro_nacional_victimas_renavi` | CEAV | 1 |
| Cuaderno Mensual Estadístico Penitenciario | `cuaderno_mensual_estadistico_penitenciario_enero_2026` | PRS | 52 |
| Bajas de personal | `bajas_personal` | SEMAR | 2 |
| Estadísticas del personal naval | `estadisticas_del_personal_naval` | SEMAR | 2 |
| Reportes de seguridad ferroviaria | `reportes_seguridad_sistema_ferroviario` | ARTF | 2 |
| Certificaciones SPF | `certificaciones_estandares_competencia` | SPF | 10 |
| Formación inicial SPF | `formacion_inicial_guardias_policias` | SPF | 10 |
| Registro Federal de Víctimas (REFEVI) | `registro_federal_victimas_refevi` | CEAV | 3 |

## Usage

### Python

#### Search within this category

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        results = await client.search("homicidio", category="seguridad")
        print(f"{results.total} datasets found")
        for ds in results.datasets:
            print(f"  {ds.slug}: {ds.title}")

asyncio.run(main())
```

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

#### Filter by institution

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

#### Most recently updated datasets

```python
import asyncio
from open_data_mexico import DatosGobMX

async def recent():
    async with DatosGobMX() as client:
        datasets = await client.get_category_datasets("seguridad")
        # datasets are ordered by most recently updated (site default)
        # ds.last_updated is a timezone-aware UTC datetime
        for ds in datasets[:5]:
            print(f"{ds.last_updated:%Y-%m-%d}  {ds.title}")

asyncio.run(recent())
```

#### Get full dataset detail

```python
import asyncio
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        detail = await client.get_dataset("incidencia_delictiva")
        print(detail.title)
        print(f"License: {detail.license_name}")
        print(f"Tags: {', '.join(detail.tags)}")
        for r in detail.resources:
            print(f"  [{r.format}] {r.name}")
            print(f"    {r.download_url}")

asyncio.run(main())
```

#### Load a CSV into pandas

```python
import asyncio
import io
import pandas as pd
from open_data_mexico import DatosGobMX

async def main():
    async with DatosGobMX() as client:
        detail = await client.get_dataset("incidencia_delictiva")
        csv_str = await client.get_resource_data(detail.resources[0])
        df = pd.read_csv(io.StringIO(csv_str))
        print(df.shape)
        print(df.head())

asyncio.run(main())
```

### REST API

```bash
# Search within the category
curl "http://localhost:8000/search?q=homicidio&category=seguridad"

# Category metadata
curl http://localhost:8000/categories/seguridad

# All datasets
curl http://localhost:8000/categories/seguridad/datasets

# Dataset detail
curl http://localhost:8000/datasets/incidencia_delictiva
```

## See also

- [All categories](../index.md)
- [Source page on datos.gob.mx](https://www.datos.gob.mx/group/seguridad)
