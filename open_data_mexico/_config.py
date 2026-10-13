BASE_URL = "https://www.datos.gob.mx"
HEADERS = {
    # Identify the library honestly. The previous Chrome impersonation caused
    # reproducible 403 responses on repodatos.atdt.gob.mx CSV downloads.
    "User-Agent": "open-data-mexico",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
}

# Seconds to wait between requests (0 = no delay). Increase to avoid hammering the site.
REQUEST_DELAY: float = 0.0

# Number of retry attempts on transient failures (5xx, 429, network errors).
MAX_RETRIES: int = 3

# Seconds to cache responses in memory (0 = disabled). 300 = 5 minutes.
CACHE_TTL: float = 300.0

# Max number of pages fetched in parallel during auto-pagination.
# Each concurrent worker still respects MAX_RETRIES and REQUEST_DELAY.
CONCURRENCY: int = 5
