"""
Internal utility functions shared across scrapers.
Not part of the public API.
"""

import re
from datetime import UTC, datetime

_ES_MONTHS: dict[str, int] = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}

_ES_DATE_RE = re.compile(r"(\d{1,2})\s+de\s+(\w+)\s+(\d{4})", re.IGNORECASE)


def parse_spanish_date(text: str | None) -> datetime | None:
    """Parse a Spanish-locale date string into a UTC-midnight datetime.

    Examples::

        parse_spanish_date("4 de junio 2025")   # → datetime(2025, 6, 4, tzinfo=UTC)
        parse_spanish_date("17 de marzo 2026")  # → datetime(2026, 3, 17, tzinfo=UTC)
        parse_spanish_date(None)                # → None

    Returns ``None`` for any input that doesn't match the expected pattern.
    """
    if not text:
        return None
    m = _ES_DATE_RE.search(text.strip())
    if not m:
        return None
    day, month_name, year = int(m.group(1)), m.group(2).lower(), int(m.group(3))
    month = _ES_MONTHS.get(month_name)
    if not month:
        return None
    return datetime(year, month, day, tzinfo=UTC)


def parse_iso_dt(text: str | None) -> datetime | None:
    """Parse an ISO 8601 datetime string, returning None on failure.

    Handles both offset-aware strings (``'2026-03-23T16:28:17+0000'``) and
    naive strings (``'2025-06-04T18:44:31.334457'``). Naive strings are
    treated as UTC.

    Examples::

        parse_iso_dt("2026-03-23T16:28:17+0000")      # → aware datetime (UTC)
        parse_iso_dt("2025-06-04T18:44:31.334457")    # → aware datetime (UTC)
        parse_iso_dt(None)                             # → None
    """
    if not text:
        return None
    try:
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt
    except (ValueError, TypeError):
        return None
