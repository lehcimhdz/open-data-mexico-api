# open-data-mexico v1.2 — Improvement Spec

> Detailed analysis of the current codebase and concrete plan for the next minor
> release. Authored 2026-06-13.

---

## 1. State of the project (audit, as of `9c79601`)

### What's solid

| Area | Status |
|---|---|
| Public Python API | `DatosGobMX` async client with 8 methods, fully typed |
| HTTP layer | `_http.robust_get()` with exponential backoff, retries 5xx/429, network errors |
| Caching | In-memory TTL cache (default 300 s) keyed per endpoint |
| Data models | 8 Pydantic v2 models, timezone-aware datetimes |
| Tests | 122 tests passing, **95.09 % coverage** (above the 90 % gate) |
| Quality tooling | ruff (lint+format), mypy, pre-commit, py.typed marker |
| CI/CD | GitHub Actions: lint+test matrix (3.11/3.12/3.13), pip-audit, nightly smoke, MkDocs deploy, PyPI publish via OIDC |
| Optional REST server | FastAPI app with lifespan-shared client, 8 endpoints |
| Documentation | README (~17 KB), MkDocs site, CHANGELOG (Keep-a-Changelog), CONTRIBUTING, SECURITY |
| Release status | `pyproject.toml` declares **1.1.0**, classifier `Production/Stable` |

### Pain points and gaps

| Issue | Evidence | Severity |
|---|---|---|
| **Version drift** — `__init__.__version__` says `"0.1.0"`, server `version="0.1.0"`, SECURITY.md only lists `0.1.x`, but `pyproject.toml` is `1.1.0` | grep `0.1.0` across `open_data_mexico/` + `server/` | High (publishing bug) |
| **Sequential page fetching** — categories with many pages (educación ≈ 71 pages of 20 datasets) are fetched one after another | `_scrapers/datasets.py:172-181` `for page in range(2, total_pages + 1)` | Medium (latency) |
| **No streaming pagination** — must wait for *all* pages before iterating | `fetch_category_datasets` returns full list | Medium |
| **No binary download path** — `get_resource_data()` always decodes to `str`, XLSX/ZIP/SHP cannot be retrieved cleanly | `client.py:286-288` `resp.content.decode("utf-8")` | Medium |
| **Pandas helper missing** — pandas is a documented optional extra but there's no shortcut, users have to write `pd.read_csv(io.StringIO(await client.get_resource_data(r)))` every time | README "Load CSV data into pandas" example | Low/UX |
| **No CLI** — pure library; users have to open Python to look up a slug | n/a | Medium |
| **Cache is opaque** — no public way to clear/inspect it | `_cache_get/_cache_set` are private; no `clear_cache()` | Low |
| **Server is minimal** — no CORS, no `/health`, hard-coded version | `server/app.py` | Low |
| **SECURITY.md outdated** | only `0.1.x` listed as supported | Low |

### Things explicitly **not** in scope for v1.2

- Geopandas / shapefile extra (PROJECT.md row, blocked by heavy deps).
- PyPI Trusted Publisher config (must be done in pypi.org UI by the maintainer).
- Persistent disk cache (in-memory TTL stays default; layered cache is a v1.3 idea).
- Splitting README into ES/EN files.

---

## 2. Release plan — v1.2.0 "Productivity & Power Users"

### 2.1 Bug fixes

1. **Version single source of truth.** Read `__version__` via `importlib.metadata.version("open-data-mexico")` with a `PackageNotFoundError` fallback. Drop the hard-coded literal in `__init__.py` and the FastAPI app constructor + `/` handler.
2. Update `SECURITY.md` supported versions table to `1.x ✅`.

### 2.2 Performance — concurrent pagination

- New constructor param `DatosGobMX(concurrency: int = 5)`. Default of 5 is polite, matches `request_delay`'s spirit.
- New helper `_fetch_pages_concurrent(client, url_builder, total_pages, *, concurrency, …)` in `_http.py` (or a dedicated `_pagination.py`).
- `fetch_all_categories()` and `fetch_category_datasets()` switch from a sequential `for` to: fetch page 1 → learn `total_pages` → `asyncio.gather` the remaining pages bounded by an `asyncio.Semaphore`.
- Output order is preserved by sorting on page index.
- `request_delay` semantics: respected per request; the semaphore + delay together give a "polite parallel" rate-limit.

### 2.3 Streaming pagination

- `async def iter_category_datasets(slug) -> AsyncIterator[Dataset]` on `DatosGobMX`. Yields page-by-page; the first page returns datasets immediately so the consumer can start processing while later pages are still in flight.

### 2.4 Binary downloads + pandas convenience

- `async def get_resource_bytes(resource) -> bytes` — raw bytes, no decoding. Use this for XLSX/ZIP/SHP.
- `async def get_resource_dataframe(resource, **read_kwargs) -> "pandas.DataFrame"` — lazy `import pandas`; dispatches on `resource.format` (`csv` → `read_csv` with utf-8 → latin-1 fallback; `xlsx`/`xls` → `read_excel` from bytes; otherwise `ValueError`). Raises `ImportError` with a helpful "install with `[pandas]`" message when pandas is missing.
- `get_resource_data()` keeps its current text-only contract — no breaking change.

### 2.5 Cache management

- `def clear_cache(self) -> None` — drops the entire dict.
- `def invalidate(self, key_prefix: str) -> int` — drops entries with a matching key prefix (returns count). Lets users clear a single category without wiping everything.

### 2.6 CLI — `open-data-mx`

- New module `open_data_mexico/cli.py`. **No new runtime dependency** — uses argparse.
- Console script registered in `pyproject.toml` `[project.scripts]`:
  ```toml
  [project.scripts]
  open-data-mx = "open_data_mexico.cli:main"
  ```
- Subcommands:
  - `open-data-mx categories` — list slug + name + count.
  - `open-data-mx category <slug>` — show details.
  - `open-data-mx datasets <slug> [--limit N]` — list datasets in a category.
  - `open-data-mx dataset <slug>` — full detail including resources.
  - `open-data-mx organizations [--limit N]`.
  - `open-data-mx organization <slug>`.
  - `open-data-mx search "..." [--category X] [--limit N] [--offset N]`.
  - `open-data-mx download <dataset_slug> [--output dir/] [--format csv]` — saves all matching resources locally.
- Global flags: `--json` (machine-readable output), `--no-color`, `--timeout`, `--delay`, `--retries`.

### 2.7 FastAPI server polish

- Add `CORSMiddleware` with `allow_origins=["*"]` default (override via `CORS_ORIGINS` env var, comma-separated).
- Add `GET /health` → `{"status": "ok", "version": "..."}`.
- Read the version dynamically (`importlib.metadata`).
- Tag endpoints in the OpenAPI spec for nicer Swagger grouping.

### 2.8 Tests

| New module | Coverage |
|---|---|
| `tests/test_cli.py` | All subcommands; JSON output; error paths |
| `tests/test_concurrency.py` | Concurrent pagination preserves order; semaphore caps in-flight requests |
| `tests/test_resource_bytes.py` | bytes path + dataframe path (mocked pandas) |
| `tests/test_iter.py` | Async iterator yields page-by-page |
| Extend `test_client.py` | `clear_cache()` / `invalidate(prefix)` semantics |
| Extend `test_search.py` (or new `test_server.py`) | CORS header present, `/health` returns 200 |

Coverage gate stays at **90 %**.

### 2.9 Docs / release hygiene

- README: new "CLI" section, new "Concurrency" subsection in Client Reference, document `get_resource_bytes` / `get_resource_dataframe` / `iter_category_datasets` / cache methods.
- CHANGELOG: add v1.2.0 section, move "Unreleased" entries.
- `pyproject.toml`: bump version `1.1.0 → 1.2.0`.

---

## 3. Execution order

```
1. Version sync (importlib.metadata)    [touch __init__.py, server/app.py, SECURITY.md, pyproject.toml]
2. Concurrent pagination helper         [_http.py extension or new _pagination.py]
3. iter_category_datasets               [client.py + _scrapers/datasets.py]
4. get_resource_bytes + dataframe       [client.py]
5. Cache management                     [client.py]
6. CLI                                  [open_data_mexico/cli.py + pyproject.toml [scripts]]
7. Server polish                        [server/app.py]
8. Tests for everything above
9. README + CHANGELOG + version bump
10. Final ruff/mypy/pytest, commit
```

---

## 4. Non-goals / invariants

- **No new runtime dependencies.** CLI uses argparse; concurrency uses stdlib `asyncio`; bytes path is pure httpx.
- **No breaking changes.** All new APIs are additive. `get_resource_data()` keeps its signature and behaviour.
- **Coverage ≥ 90 %.** All new code paths must be tested.
- **Polite by default.** Default concurrency = 5, default `request_delay = 0`, but the two compose so users can ship `DatosGobMX(concurrency=10, request_delay=0.2)` for big jobs.
