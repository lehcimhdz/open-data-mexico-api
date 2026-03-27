# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [1.0.0] — 2026-03-27

### Added
- `request_delay` parameter on `DatosGobMX` for configurable rate limiting between requests.
- `max_retries` parameter on `DatosGobMX` for automatic retry with exponential backoff on 5xx/429 and network errors.
- `cache_ttl` parameter on `DatosGobMX` for in-memory TTL caching of responses (default 300 s).
- `open_data_mexico/_http.py` — `robust_get()` helper used by all scrapers.
- FastAPI server uses a single shared `DatosGobMX` client via lifespan (connection pool + shared cache).
- `py.typed` marker for PEP 561 compliance (mypy/pyright support).
- GitHub Actions CI workflow — lint, type-check and test on Python 3.11, 3.12, 3.13.
- GitHub Actions publish workflow — build and publish to PyPI on GitHub Release via OIDC Trusted Publisher.
- `.pre-commit-config.yaml` with ruff and mypy hooks.
- `pytest-cov` with 80 % minimum coverage enforced.
- MkDocs site configuration.
- `client.search(query)` — full-text dataset search via CKAN `package_search` JSON API; supports `category`, `limit`, `offset` parameters; returns `SearchResponse`.
- `client.get_organizations()` — lists all 184+ publishing institutions via CKAN `organization_list`; returns `list[Organization]`.
- `client.get_organization(slug)` — fetches a single organization by slug via CKAN `organization_show`; returns `None` on 404.
- `Organization` and `OrganizationsResponse` Pydantic models.
- `SearchResponse` Pydantic model.
- `GET /organizations` and `GET /organizations/{slug}` FastAPI endpoints.
- `GET /search?q=...` FastAPI endpoint with optional `category`, `limit`, `offset` query params.
- `open_data_mexico/_utils.py` — `parse_spanish_date()` and `parse_iso_dt()` helpers for robust datetime parsing.

### Changed
- `_get_total_pages()` now scans all `<li>` elements in `ul.pagination` instead of only `<a>` tags, making pagination detection more robust against disabled/active page items rendered as `<span>`.
- `Dataset.last_updated`, `DatasetDetail.created`, and `DatasetDetail.last_updated` changed from `str | None` to `datetime | None`; values are now timezone-aware UTC datetimes.
- `pyproject.toml`: corrected project URLs to the real GitHub repository.
- `pyproject.toml`: `license` field now points to the `LICENSE` file.
- `pyproject.toml`: added Python 3.13 classifier.
- README updated to document new client parameters and corrected test count.

### Fixed
- Unused imports removed across `client.py`, `server/app.py`, and test files (ruff F401).
- `Optional[str]` annotations modernised to `str | None` (ruff UP045).

---

## [0.1.0] — 2026-03-23

### Added
- Initial implementation of `DatosGobMX` async client.
- Scraping of categories (`/group/`), dataset listings (`/group/{slug}`), and dataset detail pages (`/dataset/{slug}`).
- Pydantic models: `Category`, `Dataset`, `DatasetDetail`, `Resource`, `CategoriesResponse`, `DatasetsResponse`.
- Auto-pagination for categories and dataset listings.
- `get_resource_data()` for in-memory CSV download with UTF-8 / latin-1 fallback.
- Optional FastAPI REST server (`pip install open-data-mexico[server]`).
- 44 tests with mock HTML fixtures (pytest-asyncio + pytest-httpx).
- Documentation for all 28 available categories.

[Unreleased]: https://github.com/lehcimhdz/open-data-mexico-api/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/lehcimhdz/open-data-mexico-api/releases/tag/v1.0.0
[0.1.0]: https://github.com/lehcimhdz/open-data-mexico-api/releases/tag/v0.1.0
