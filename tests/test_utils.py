"""Tests for open_data_mexico._utils date-parsing helpers."""
from datetime import UTC, datetime

import pytest

from open_data_mexico._utils import parse_iso_dt, parse_spanish_date


# ---------------------------------------------------------------------------
# parse_spanish_date
# ---------------------------------------------------------------------------

class TestParseSpanishDate:
    def test_valid_date(self):
        assert parse_spanish_date("4 de junio 2025") == datetime(2025, 6, 4, tzinfo=UTC)

    def test_none_returns_none(self):
        assert parse_spanish_date(None) is None

    def test_empty_string_returns_none(self):
        assert parse_spanish_date("") is None

    def test_no_match_returns_none(self):
        """English-style date — no match for the Spanish regex."""
        assert parse_spanish_date("June 4 2025") is None

    def test_invalid_month_name_returns_none(self):
        assert parse_spanish_date("4 de foobar 2025") is None

    def test_whitespace_only_returns_none(self):
        assert parse_spanish_date("   ") is None

    def test_case_insensitive_month(self):
        assert parse_spanish_date("17 de Marzo 2026") == datetime(2026, 3, 17, tzinfo=UTC)

    @pytest.mark.parametrize("month_name,month_num", [
        ("enero", 1), ("febrero", 2), ("marzo", 3), ("abril", 4),
        ("mayo", 5), ("junio", 6), ("julio", 7), ("agosto", 8),
        ("septiembre", 9), ("octubre", 10), ("noviembre", 11), ("diciembre", 12),
    ])
    def test_all_twelve_months(self, month_name: str, month_num: int):
        result = parse_spanish_date(f"1 de {month_name} 2024")
        assert result == datetime(2024, month_num, 1, tzinfo=UTC)

    def test_single_digit_day(self):
        assert parse_spanish_date("7 de agosto 2023") == datetime(2023, 8, 7, tzinfo=UTC)

    def test_two_digit_day(self):
        assert parse_spanish_date("31 de diciembre 2024") == datetime(2024, 12, 31, tzinfo=UTC)

    def test_returns_utc_midnight(self):
        result = parse_spanish_date("1 de enero 2026")
        assert result is not None
        assert result.hour == 0 and result.minute == 0 and result.second == 0
        assert result.tzinfo == UTC


# ---------------------------------------------------------------------------
# parse_iso_dt
# ---------------------------------------------------------------------------

class TestParseIsoDt:
    def test_offset_aware_string(self):
        result = parse_iso_dt("2026-03-23T16:28:17+0000")
        assert result is not None
        assert result.tzinfo is not None
        assert result == datetime(2026, 3, 23, 16, 28, 17, tzinfo=UTC)

    def test_naive_string_gets_utc(self):
        result = parse_iso_dt("2025-06-04T18:44:31.334457")
        assert result is not None
        assert result.tzinfo == UTC
        assert result.year == 2025 and result.month == 6 and result.day == 4

    def test_none_returns_none(self):
        assert parse_iso_dt(None) is None

    def test_empty_string_returns_none(self):
        assert parse_iso_dt("") is None

    def test_invalid_string_returns_none(self):
        assert parse_iso_dt("not-a-date") is None

    def test_out_of_range_date_returns_none(self):
        """fromisoformat raises ValueError for invalid calendar dates."""
        assert parse_iso_dt("2026-99-99T00:00:00") is None

    def test_iso_with_timezone_offset(self):
        result = parse_iso_dt("2026-01-15T12:00:00+05:30")
        assert result is not None
        assert result.tzinfo is not None
