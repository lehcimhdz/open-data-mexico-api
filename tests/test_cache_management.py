"""Tests for the public cache-management API: clear_cache and invalidate."""

from time import monotonic

from open_data_mexico import DatosGobMX


def test_clear_cache_drops_all_entries():
    client = DatosGobMX(cache_ttl=60)
    client._cache_set("categories", ["a"])
    client._cache_set("dataset:incidencia_delictiva", "x")
    assert client._cache  # populated

    client.clear_cache()
    assert client._cache == {}


def test_invalidate_returns_count_of_removed_entries():
    client = DatosGobMX(cache_ttl=60)
    client._cache_set("datasets:salud", ["a"])
    client._cache_set("datasets:seguridad", ["b"])
    client._cache_set("dataset:rezago_social", "x")

    removed = client.invalidate("datasets:")
    assert removed == 2
    assert "datasets:salud" not in client._cache
    assert "datasets:seguridad" not in client._cache
    assert "dataset:rezago_social" in client._cache


def test_invalidate_no_match_returns_zero():
    client = DatosGobMX(cache_ttl=60)
    client._cache_set("categories", ["a"])
    assert client.invalidate("nonexistent:") == 0
    assert client._cache  # untouched


def test_invalidate_exact_key_match():
    client = DatosGobMX(cache_ttl=60)
    client._cache["datasets:seguridad"] = (monotonic() + 60, ["a"])
    removed = client.invalidate("datasets:seguridad")
    assert removed == 1
    assert "datasets:seguridad" not in client._cache
