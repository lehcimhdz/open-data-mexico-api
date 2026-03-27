# Contributing to open-data-mexico

Thank you for your interest in contributing! This document covers everything you need to get started.

---

## Setup

**Requirements:** Python 3.11+ and git.

```bash
git clone https://github.com/lehcimhdz/open-data-mexico-api.git
cd open-data-mexico-api
pip install -e ".[dev]"
```

Install pre-commit hooks so linting runs automatically before every commit:

```bash
pip install pre-commit
pre-commit install
```

---

## Running tests

```bash
# Full suite with coverage (must stay above 80 %)
pytest

# Skip coverage for a faster feedback loop
pytest --no-cov -v

# Single file
pytest tests/test_datasets.py -v
```

---

## Code quality

All three checks must pass before opening a PR — they also run in CI:

```bash
ruff check .          # lint
ruff format --check . # formatting
mypy open_data_mexico/ --ignore-missing-imports  # type checking
```

Auto-fix lint and formatting issues:

```bash
ruff check . --fix
ruff format .
```

---

## Project structure

```
open_data_mexico/        # installable library (published to PyPI)
├── client.py            # DatosGobMX — public entry point
├── models.py            # Pydantic models
├── _config.py           # BASE_URL, headers, defaults (private)
├── _http.py             # robust_get() with retry/backoff (private)
└── _scrapers/           # HTML scraping internals (private)
    ├── categories.py
    ├── datasets.py
    └── dataset_detail.py
server/                  # optional FastAPI REST server
tests/                   # pytest suite with mock HTML fixtures
docs/                    # MkDocs source
```

---

## Making changes

### Scraper changes

The scrapers parse HTML from `datos.gob.mx`. If the site changes its structure, update the CSS selectors and add/update the corresponding HTML fixture in `tests/conftest.py` to reflect the new markup.

### Adding a new public method

1. Implement it in `client.py`.
2. Export it from `open_data_mexico/__init__.py` and add it to `__all__`.
3. Add a Pydantic model in `models.py` if the method returns a new type.
4. Write tests in `tests/`.
5. Document it in `README.md` (Client Reference section).

### Updating the CHANGELOG

Add a bullet under `## [Unreleased]` in `CHANGELOG.md` following the [Keep a Changelog](https://keepachangelog.com) convention (`Added`, `Changed`, `Fixed`, `Removed`).

---

## Pull request checklist

- [ ] `pytest` passes with ≥ 80 % coverage
- [ ] `ruff check .` reports no errors
- [ ] `ruff format --check .` reports no changes needed
- [ ] `mypy open_data_mexico/` reports no errors
- [ ] `CHANGELOG.md` updated under `[Unreleased]`
- [ ] New public API documented in `README.md`

---

## Reporting bugs

Open an issue at [github.com/lehcimhdz/open-data-mexico-api/issues](https://github.com/lehcimhdz/open-data-mexico-api/issues) with:
- Python version and OS
- Minimal code that reproduces the problem
- Full traceback if applicable
