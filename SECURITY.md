# Security Policy

## Supported versions

Only the latest released version receives security fixes.

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅ Yes    |

## Reporting a vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Report vulnerabilities privately via GitHub's
[Security Advisories](https://github.com/lehcimhdz/open-data-mexico-api/security/advisories/new)
feature (Repository → Security → Report a vulnerability).

Include:
- A description of the vulnerability and its potential impact.
- Steps to reproduce it.
- Any suggested fix if you have one.

You will receive an acknowledgement within 48 hours and a status update within 7 days.

## Scope

This library is a read-only HTTP scraper. It makes GET requests to a public government website and returns parsed data. There are no write operations, no authentication flows, and no user data is stored.

Potential areas of concern relevant to this project:

- **Dependency vulnerabilities** in `httpx`, `beautifulsoup4`, `lxml`, or `pydantic`.
- **Malicious content** injected into the scraped HTML that could affect downstream consumers of the parsed data.
- **Unsafe URL handling** if a resource's `download_url` points to an unexpected host.
