"""Tests for the streaming iter_category_datasets() async generator."""

from pytest_httpx import HTTPXMock

from open_data_mexico import DatosGobMX

_DATASET_HTML_TEMPLATE = """
<html><body>
<ul class="pagination">
  <li>1</li><li>2</li>
</ul>
<ul class="dataset-list">
  <li class="resource-item">
    <h3><a class="text-black" href="/dataset/{slug}">{title}</a></h3>
  </li>
</ul>
</body></html>
"""


async def test_iter_category_datasets_yields_in_page_order(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/group/salud",
        text=_DATASET_HTML_TEMPLATE.format(slug="ds_a", title="DS A"),
    )
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/group/salud?page=2",
        text=_DATASET_HTML_TEMPLATE.format(slug="ds_b", title="DS B"),
    )

    async with DatosGobMX() as client:
        out = [ds async for ds in client.iter_category_datasets("salud")]

    assert [d.slug for d in out] == ["ds_a", "ds_b"]


async def test_iter_category_datasets_supports_early_break(httpx_mock: HTTPXMock):
    """Consumer stops after page 1 — page 2 is never requested."""
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/group/salud",
        text=_DATASET_HTML_TEMPLATE.format(slug="ds_a", title="DS A"),
    )
    # No mock for page 2 → if it's requested, httpx_mock would raise.

    async with DatosGobMX() as client:
        out = []
        async for ds in client.iter_category_datasets("salud"):
            out.append(ds)
            break

    assert [d.slug for d in out] == ["ds_a"]


async def test_iter_category_datasets_without_context_manager(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/group/salud",
        text=_DATASET_HTML_TEMPLATE.format(slug="ds_a", title="DS A"),
    )
    httpx_mock.add_response(
        url="https://www.datos.gob.mx/group/salud?page=2",
        text=_DATASET_HTML_TEMPLATE.format(slug="ds_b", title="DS B"),
    )

    client = DatosGobMX()
    out = [ds async for ds in client.iter_category_datasets("salud")]
    assert [d.slug for d in out] == ["ds_a", "ds_b"]
    assert client._client is None  # closed on exit
