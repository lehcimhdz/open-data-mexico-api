"""Tests for the open-data-mx CLI."""

import json
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import AsyncMock, patch

from open_data_mexico import (
    Category,
    Dataset,
    DatasetDetail,
    Organization,
    SearchResponse,
)
from open_data_mexico.cli import main
from open_data_mexico.models import Resource

_CATS = [
    Category(slug="salud", name="Salud", url="https://x", dataset_count=10),
    Category(slug="seguridad", name="Seguridad", url="https://x", dataset_count=20),
]

_DS = Dataset(
    slug="rezago_social",
    title="Rezago social",
    last_updated=datetime(2025, 6, 4, tzinfo=UTC),
    url="https://x",
)

_DETAIL = DatasetDetail(
    slug="incidencia_delictiva",
    title="Incidencia delictiva",
    url="https://x",
    tags=["Homicidio doloso"],
    resources=[
        Resource(
            resource_id="r1",
            name="Incidencia CSV",
            format="csv",
            download_url="https://example.com/data.csv",
        )
    ],
)

_ORGS = [Organization(slug="coneval", title="CONEVAL", url="https://x", dataset_count=2)]


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------


def test_no_args_prints_help_and_exits(capsys):
    try:
        main([])
    except SystemExit as e:
        assert e.code == 2  # argparse "command is required"
    err = capsys.readouterr().err
    assert "command" in err


def test_version_flag(capsys):
    try:
        main(["--version"])
    except SystemExit as e:
        assert e.code == 0
    out = capsys.readouterr().out
    assert "open-data-mx" in out


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------


def test_categories_text_output(capsys):
    with patch("open_data_mexico.cli.DatosGobMX.get_categories", new=AsyncMock(return_value=_CATS)):
        code = main(["categories"])
    assert code == 0
    out = capsys.readouterr().out
    assert "salud" in out and "Salud" in out
    assert "seguridad" in out


def test_categories_json_output(capsys):
    with patch("open_data_mexico.cli.DatosGobMX.get_categories", new=AsyncMock(return_value=_CATS)):
        code = main(["--json", "categories"])
    assert code == 0
    data = json.loads(capsys.readouterr().out)
    assert len(data) == 2
    assert data[0]["slug"] == "salud"


# ---------------------------------------------------------------------------
# Category (single)
# ---------------------------------------------------------------------------


def test_category_found(capsys):
    with patch(
        "open_data_mexico.cli.DatosGobMX.get_category", new=AsyncMock(return_value=_CATS[0])
    ):
        code = main(["category", "salud"])
    assert code == 0
    assert "Salud" in capsys.readouterr().out


def test_category_not_found(capsys):
    with patch("open_data_mexico.cli.DatosGobMX.get_category", new=AsyncMock(return_value=None)):
        code = main(["category", "nope"])
    assert code == 1
    assert "not found" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# Datasets / dataset
# ---------------------------------------------------------------------------


def test_datasets_listing_with_limit(capsys):
    datasets = [_DS, Dataset(slug="b", title="B", url="x")]
    with patch(
        "open_data_mexico.cli.DatosGobMX.get_category_datasets",
        new=AsyncMock(return_value=datasets),
    ):
        code = main(["datasets", "poblacion", "--limit", "1"])
    assert code == 0
    out = capsys.readouterr().out
    assert "rezago_social" in out
    assert "B" not in out  # truncated


def test_dataset_detail(capsys):
    with patch("open_data_mexico.cli.DatosGobMX.get_dataset", new=AsyncMock(return_value=_DETAIL)):
        code = main(["dataset", "incidencia_delictiva"])
    assert code == 0
    out = capsys.readouterr().out
    assert "Incidencia delictiva" in out
    assert "Incidencia CSV" in out


def test_dataset_not_found(capsys):
    with patch("open_data_mexico.cli.DatosGobMX.get_dataset", new=AsyncMock(return_value=None)):
        code = main(["dataset", "nope"])
    assert code == 1


# ---------------------------------------------------------------------------
# Organizations
# ---------------------------------------------------------------------------


def test_organizations_listing(capsys):
    with patch(
        "open_data_mexico.cli.DatosGobMX.get_organizations",
        new=AsyncMock(return_value=_ORGS),
    ):
        code = main(["organizations"])
    assert code == 0
    assert "coneval" in capsys.readouterr().out


def test_organization_not_found(capsys):
    with patch(
        "open_data_mexico.cli.DatosGobMX.get_organization",
        new=AsyncMock(return_value=None),
    ):
        code = main(["organization", "nope"])
    assert code == 1


def test_organization_found(capsys):
    with patch(
        "open_data_mexico.cli.DatosGobMX.get_organization",
        new=AsyncMock(return_value=_ORGS[0]),
    ):
        code = main(["organization", "coneval"])
    assert code == 0
    assert "CONEVAL" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------


def test_search_text_output(capsys):
    resp = SearchResponse(total=1, query="rezago", category=None, offset=0, datasets=[_DS])
    with patch("open_data_mexico.cli.DatosGobMX.search", new=AsyncMock(return_value=resp)):
        code = main(["search", "rezago"])
    assert code == 0
    out = capsys.readouterr().out
    assert "rezago_social" in out
    assert "1 matches" in out


def test_search_json_output(capsys):
    resp = SearchResponse(total=1, query="rezago", category=None, offset=0, datasets=[_DS])
    with patch("open_data_mexico.cli.DatosGobMX.search", new=AsyncMock(return_value=resp)):
        code = main(["--json", "search", "rezago"])
    assert code == 0
    data = json.loads(capsys.readouterr().out)
    assert data["total"] == 1
    assert data["query"] == "rezago"


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------


def test_download_saves_resources(tmp_path: Path, capsys):
    payload = b"col1,col2\n1,2\n"
    with patch("open_data_mexico.cli.DatosGobMX.get_dataset", new=AsyncMock(return_value=_DETAIL)):
        with patch(
            "open_data_mexico.cli.DatosGobMX.get_resource_bytes",
            new=AsyncMock(return_value=payload),
        ):
            code = main(["download", "incidencia_delictiva", "--output", str(tmp_path)])
    assert code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 1
    assert files[0].read_bytes() == payload
    assert "saved 1" in capsys.readouterr().out


def test_download_filters_by_format(tmp_path: Path, capsys):
    with patch("open_data_mexico.cli.DatosGobMX.get_dataset", new=AsyncMock(return_value=_DETAIL)):
        with patch(
            "open_data_mexico.cli.DatosGobMX.get_resource_bytes", new=AsyncMock(return_value=b"x")
        ):
            code = main(
                [
                    "download",
                    "incidencia_delictiva",
                    "--output",
                    str(tmp_path),
                    "--format",
                    "xlsx",  # no matching resource
                ]
            )
    assert code == 1
    assert "no downloadable" in capsys.readouterr().err


def test_download_dataset_not_found(tmp_path: Path, capsys):
    with patch("open_data_mexico.cli.DatosGobMX.get_dataset", new=AsyncMock(return_value=None)):
        code = main(["download", "nope", "--output", str(tmp_path)])
    assert code == 1
