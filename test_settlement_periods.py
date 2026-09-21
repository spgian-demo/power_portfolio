"""Lecture 4.1: Check time calculations, labels and the updated report."""

from datetime import date, datetime, timedelta

import pytest

from main import main
from settlement_periods import settlement_period_label, settlement_period_times


def test_first_settlement_period_times() -> None:
    start_time, end_time = settlement_period_times(date(2026, 9, 1), 1)

    assert start_time == datetime(2026, 9, 1, 0, 0)
    assert end_time == datetime(2026, 9, 1, 0, 30)
    assert settlement_period_label(date(2026, 9, 1), 1) == "00:00-00:30"


def test_existing_period_times_and_labels() -> None:
    # Fixed expectations for the three records already used in main.py.
    expected = [
        (25, datetime(2026, 9, 1, 12, 0), datetime(2026, 9, 1, 12, 30),
         "12:00-12:30"),
        (26, datetime(2026, 9, 1, 12, 30), datetime(2026, 9, 1, 13, 0),
         "12:30-13:00"),
        (27, datetime(2026, 9, 1, 13, 0), datetime(2026, 9, 1, 13, 30),
         "13:00-13:30"),
    ]
    for number, expected_start, expected_end, expected_label in expected:
        assert settlement_period_times(date(2026, 9, 1), number) == (
            expected_start, expected_end
        )
        assert settlement_period_label(date(2026, 9, 1), number) == expected_label


def test_last_period_ends_on_next_date() -> None:
    start_time, end_time = settlement_period_times(date(2026, 9, 1), 48)

    assert start_time == datetime(2026, 9, 1, 23, 30)
    assert end_time == datetime(2026, 9, 2, 0, 0)
    assert end_time - start_time == timedelta(minutes=30)
    assert settlement_period_label(date(2026, 9, 1), 48) == (
        "23:30-00:00 (+1 day)"
    )


def test_last_period_rolls_into_next_year() -> None:
    start_time, end_time = settlement_period_times(date(2026, 12, 31), 48)

    assert start_time == datetime(2026, 12, 31, 23, 30)
    assert end_time == datetime(2027, 1, 1, 0, 0)
    assert settlement_period_label(date(2026, 12, 31), 48) == (
        "23:30-00:00 (+1 day)"
    )


def test_all_periods_are_adjacent_and_half_hour_long() -> None:
    # Test the clock grid without generating any electricity or price data.
    previous_end = datetime(2026, 9, 1, 0, 0)

    for number in range(1, 49):
        start_time, end_time = settlement_period_times(date(2026, 9, 1), number)
        assert start_time == previous_end
        assert end_time - start_time == timedelta(minutes=30)
        previous_end = end_time

    assert previous_end == datetime(2026, 9, 2, 0, 0)


def test_rejects_out_of_range_periods() -> None:
    for number in (0, 49):
        with pytest.raises(ValueError, match="between 1 and 48"):
            settlement_period_times(date(2026, 9, 1), number)
        with pytest.raises(ValueError, match="between 1 and 48"):
            settlement_period_label(date(2026, 9, 1), number)


def test_rejects_invalid_period_types() -> None:
    # Wrong types are intentional here. Even 25.0 is not an int.
    for number in (25.0, 25.5, True, "25"):
        with pytest.raises(TypeError, match="must be an integer"):
            settlement_period_times(date(2026, 9, 1), number)  # type: ignore[arg-type]


def test_requires_a_date_object() -> None:
    # A date string or datetime is not the date-only object this helper requires.
    for invalid_date in ("2026-09-01", datetime(2026, 9, 1, 0, 0)):
        with pytest.raises(TypeError, match="must be a datetime.date object"):
            settlement_period_times(invalid_date, 25)  # type: ignore[arg-type]


def test_report_shows_time_labels(capsys: pytest.CaptureFixture[str]) -> None:
    # capsys captures text printed by main(), supplied automatically by pytest.
    main()
    output = capsys.readouterr().out

    assert "POWER PORTFOLIO: 48 SETTLEMENT PERIODS" in output
    assert "Delivery date: 2026-09-01" in output
    assert "SETTLEMENT PERIOD 1 | 00:00-00:30" in output
    assert "SETTLEMENT PERIOD 25 | 12:00-12:30" in output
    assert "SETTLEMENT PERIOD 26 | 12:30-13:00" in output
    assert "SETTLEMENT PERIOD 27 | 13:00-13:30" in output
    assert "SETTLEMENT PERIOD 48 | 23:30-00:00 (+1 day)" in output
    assert "TOTALS FOR THESE 48 PERIODS ONLY" in output
    assert "Total net market cash flow:" in output
    assert output.count("\nSETTLEMENT PERIOD ") == 48
