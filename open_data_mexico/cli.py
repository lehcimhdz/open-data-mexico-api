"""
Command-line interface for the open-data-mexico client.

Installed as ``open-data-mx`` when the package is installed::

    open-data-mx --help
    open-data-mx categories
    open-data-mx search "rezago social" --limit 5
    open-data-mx dataset incidencia_delictiva
    open-data-mx download incidencia_delictiva --output ./data --format csv

Pure stdlib (argparse + asyncio). No extra dependency.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

from open_data_mexico import DatosGobMX, __version__
from open_data_mexico.models import Resource

# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------


def _stdout(text: str) -> None:
    print(text)


def _stderr(text: str) -> None:
    print(text, file=sys.stderr)


def _emit_json(payload: Any) -> None:
    """Print *payload* as pretty JSON, handling Pydantic models gracefully."""

    def _default(o: Any) -> Any:
        if hasattr(o, "model_dump"):
            return o.model_dump(mode="json")
        if hasattr(o, "isoformat"):
            return o.isoformat()
        raise TypeError(f"not serializable: {type(o)!r}")

    _stdout(json.dumps(payload, indent=2, ensure_ascii=False, default=_default))


def _fmt_date(dt: Any) -> str:
    return dt.strftime("%Y-%m-%d") if dt else "—"


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------


async def _cmd_categories(client: DatosGobMX, args: argparse.Namespace) -> int:
    categories = await client.get_categories()
    if args.json:
        _emit_json([c.model_dump(mode="json") for c in categories])
        return 0
    _stdout(f"{len(categories)} categories\n")
    for c in categories:
        _stdout(f"  {c.slug:30s}  {c.dataset_count:>5d}  {c.name}")
    return 0


async def _cmd_category(client: DatosGobMX, args: argparse.Namespace) -> int:
    cat = await client.get_category(args.slug)
    if cat is None:
        _stderr(f"category '{args.slug}' not found")
        return 1
    if args.json:
        _emit_json(cat.model_dump(mode="json"))
        return 0
    _stdout(f"{cat.name}  ({cat.slug})")
    _stdout(f"  datasets: {cat.dataset_count}")
    _stdout(f"  url:      {cat.url}")
    if cat.description:
        _stdout(f"  desc:     {cat.description}")
    return 0


async def _cmd_datasets(client: DatosGobMX, args: argparse.Namespace) -> int:
    datasets = await client.get_category_datasets(args.slug)
    if args.limit:
        datasets = datasets[: args.limit]
    if args.json:
        _emit_json([d.model_dump(mode="json") for d in datasets])
        return 0
    _stdout(f"{len(datasets)} datasets in '{args.slug}'\n")
    for d in datasets:
        _stdout(f"  {_fmt_date(d.last_updated)}  {d.slug:40s}  {d.title}")
    return 0


async def _cmd_dataset(client: DatosGobMX, args: argparse.Namespace) -> int:
    detail = await client.get_dataset(args.slug)
    if detail is None:
        _stderr(f"dataset '{args.slug}' not found")
        return 1
    if args.json:
        _emit_json(detail.model_dump(mode="json"))
        return 0
    _stdout(f"{detail.title}  ({detail.slug})")
    _stdout(f"  organization: {detail.organization_name or '—'}")
    _stdout(f"  license:      {detail.license_name or '—'}")
    _stdout(f"  updated:      {_fmt_date(detail.last_updated)}")
    if detail.tags:
        _stdout(f"  tags:         {', '.join(detail.tags)}")
    _stdout(f"  resources:    {len(detail.resources)}")
    for r in detail.resources:
        _stdout(f"    [{r.format or '?'}] {r.name}")
        if r.download_url:
            _stdout(f"      → {r.download_url}")
    return 0


async def _cmd_organizations(client: DatosGobMX, args: argparse.Namespace) -> int:
    orgs = await client.get_organizations()
    if args.limit:
        orgs = orgs[: args.limit]
    if args.json:
        _emit_json([o.model_dump(mode="json") for o in orgs])
        return 0
    _stdout(f"{len(orgs)} organizations\n")
    for o in orgs:
        _stdout(f"  {o.slug:30s}  {o.dataset_count:>5d}  {o.title}")
    return 0


async def _cmd_organization(client: DatosGobMX, args: argparse.Namespace) -> int:
    org = await client.get_organization(args.slug)
    if org is None:
        _stderr(f"organization '{args.slug}' not found")
        return 1
    if args.json:
        _emit_json(org.model_dump(mode="json"))
        return 0
    _stdout(f"{org.title}  ({org.slug})")
    _stdout(f"  datasets: {org.dataset_count}")
    _stdout(f"  url:      {org.url}")
    if org.description:
        _stdout(f"  desc:     {org.description}")
    return 0


async def _cmd_search(client: DatosGobMX, args: argparse.Namespace) -> int:
    resp = await client.search(
        args.query,
        category=args.category,
        limit=args.limit,
        offset=args.offset,
    )
    if args.json:
        _emit_json(resp.model_dump(mode="json"))
        return 0
    _stdout(f"{resp.total} matches for {resp.query!r} (showing {len(resp.datasets)})\n")
    for d in resp.datasets:
        _stdout(f"  {_fmt_date(d.last_updated)}  {d.slug:40s}  {d.title}")
    return 0


async def _cmd_download(client: DatosGobMX, args: argparse.Namespace) -> int:
    detail = await client.get_dataset(args.slug)
    if detail is None:
        _stderr(f"dataset '{args.slug}' not found")
        return 1

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    fmt_filter = args.format.lower() if args.format else None
    selected = [
        r
        for r in detail.resources
        if r.download_url and (not fmt_filter or (r.format or "").lower() == fmt_filter)
    ]
    if not selected:
        _stderr(
            f"no downloadable resources matched (format filter={fmt_filter!r}). "
            f"Dataset has {len(detail.resources)} resource(s)."
        )
        return 1

    saved = 0
    for r in selected:
        target = _safe_filename(output, r, args.slug)
        _stderr(f"  downloading {r.name} → {target}")
        data = await client.get_resource_bytes(r)
        target.write_bytes(data)
        saved += 1

    _stdout(f"saved {saved} resource(s) to {output}")
    return 0


def _safe_filename(directory: Path, resource: Resource, dataset_slug: str) -> Path:
    """Pick a filesystem-safe path for *resource* under *directory*."""
    raw = resource.name or resource.resource_id or "resource"
    safe = "".join(c if c.isalnum() or c in ("-", "_", ".") else "_" for c in raw).strip("_")
    if not safe:
        safe = resource.resource_id or "resource"
    ext = (resource.format or "").lower()
    if ext and not safe.lower().endswith(f".{ext}"):
        safe = f"{safe}.{ext}"
    return directory / f"{dataset_slug}__{safe}"


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="open-data-mx",
        description="Command-line interface for datos.gob.mx",
    )
    p.add_argument("--version", action="version", version=f"open-data-mx {__version__}")
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON output.")
    p.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout in seconds.")
    p.add_argument("--delay", type=float, default=0.0, help="Polite delay between requests.")
    p.add_argument("--retries", type=int, default=3, help="Retry attempts on 5xx/429.")
    p.add_argument("--concurrency", type=int, default=5, help="Max parallel page fetches.")

    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("categories", help="List all 28 thematic categories.")

    cat = sub.add_parser("category", help="Show one category by slug.")
    cat.add_argument("slug")

    ds_list = sub.add_parser("datasets", help="List datasets in a category.")
    ds_list.add_argument("slug")
    ds_list.add_argument("--limit", type=int, default=0, help="Truncate output to N rows.")

    ds = sub.add_parser("dataset", help="Show one dataset by slug (incl. resources).")
    ds.add_argument("slug")

    orgs = sub.add_parser("organizations", help="List all publishing organizations.")
    orgs.add_argument("--limit", type=int, default=0)

    org = sub.add_parser("organization", help="Show one organization by slug.")
    org.add_argument("slug")

    s = sub.add_parser("search", help="Full-text search across all datasets.")
    s.add_argument("query")
    s.add_argument("--category", default=None, help="Restrict to a category slug.")
    s.add_argument("--limit", type=int, default=20)
    s.add_argument("--offset", type=int, default=0)

    dl = sub.add_parser("download", help="Download every resource of a dataset.")
    dl.add_argument("slug")
    dl.add_argument("--output", default=os.getcwd(), help="Directory to write into.")
    dl.add_argument(
        "--format", default=None, help="Only download resources with this format (e.g. csv)."
    )

    return p


_DISPATCH = {
    "categories": _cmd_categories,
    "category": _cmd_category,
    "datasets": _cmd_datasets,
    "dataset": _cmd_dataset,
    "organizations": _cmd_organizations,
    "organization": _cmd_organization,
    "search": _cmd_search,
    "download": _cmd_download,
}


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------


async def _run(args: argparse.Namespace) -> int:
    handler = _DISPATCH[args.command]
    async with DatosGobMX(
        timeout=args.timeout,
        request_delay=args.delay,
        max_retries=args.retries,
        concurrency=args.concurrency,
    ) as client:
        return await handler(client, args)


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        return asyncio.run(_run(args))
    except KeyboardInterrupt:  # pragma: no cover - hard to fake in CI
        _stderr("aborted")
        return 130


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
