import pytest

from main import (
    calculate_portfolio_period,
    calculate_portfolio_periods,
    summarise_period_results,
)


def test_short_portfolio_cash_flow() -> None:
    """Check the known example: buy 2 MWh at 80 GBP/MWh."""

    # Inputs for this test.
    wind_mwh = 8.0
    solar_mwh = 2.0
    demand_mwh = 12.0
    price_gbp_per_mwh = 80.0

    result = calculate_portfolio_period(
        wind_mwh=wind_mwh,
        solar_mwh=solar_mwh,
        demand_mwh=demand_mwh,
        price_gbp_per_mwh=price_gbp_per_mwh,
    )

    # Compare with results established by hand before running the test.
    # 10 MWh generation; 12 MWh consumption; buy the 2 MWh shortage.
    # A 160 GBP purchase and no sale . Ie: -160 GBP net cash flow.
    # For numbers, allow only a tiny absolute floating-point tolerance.
    assert result["total_generation_mwh"] == pytest.approx(10.0, rel=0, abs=1e-9)
    assert result["net_position_mwh"] == pytest.approx(-2.0, rel=0, abs=1e-9)
    assert result["position"] == "SHORT"
    assert result["purchase_mwh"] == pytest.approx(2.0, rel=0, abs=1e-9)
    assert result["sale_mwh"] == pytest.approx(0.0, rel=0, abs=1e-9)
    assert result["purchase_cost_gbp"] == pytest.approx(160.0, rel=0, abs=1e-9)
    assert result["sale_revenue_gbp"] == pytest.approx(0.0, rel=0, abs=1e-9)
    assert result["net_market_cash_flow_gbp"] == pytest.approx(
        -160.0, rel=0, abs=1e-9
    )

def test_three_period_results_and_totals() -> None:
    """Check each period and the aggregate against hand-calculated values."""
    period_inputs: list[dict[str, int | float]] = [
        {
            "settlement_period": 25,
            "wind_mwh": 8.0,
            "solar_mwh": 2.0,
            "demand_mwh": 12.0,
            "price_gbp_per_mwh": 80.0,
        },
        {
            "settlement_period": 26,
            "wind_mwh": 12.0,
            "solar_mwh": 2.0,
            "demand_mwh": 12.0,
            "price_gbp_per_mwh": 100.0,
        },
        {
            "settlement_period": 27,
            "wind_mwh": 10.0,
            "solar_mwh": 2.0,
            "demand_mwh": 12.0,
            "price_gbp_per_mwh": 60.0,
        },
    ]

    results = calculate_portfolio_periods(period_inputs)

    assert len(results) == 3
    assert [r["settlement_period"] for r in results] == [25, 26, 27]
    assert [r["position"] for r in results] == ["SHORT", "LONG", "BALANCED"]

    # Check each period, so incorrect rows cannot be hidden by the totals.
    expected_by_period = {
        "total_generation_mwh": [10.0, 14.0, 12.0],
        "net_position_mwh": [-2.0, 2.0, 0.0],
        "purchase_mwh": [2.0, 0.0, 0.0],
        "sale_mwh": [0.0, 2.0, 0.0],
        "price_gbp_per_mwh": [80.0, 100.0, 60.0],
        "purchase_cost_gbp": [160.0, 0.0, 0.0],
        "sale_revenue_gbp": [0.0, 200.0, 0.0],
        "net_market_cash_flow_gbp": [-160.0, 200.0, 0.0],
    }
    for field, expected_values in expected_by_period.items():
        actual_values = [result[field] for result in results]
        assert actual_values == pytest.approx(
            expected_values, rel=0, abs=1e-9
        ), field

    totals = summarise_period_results(results)

    expected_totals = {
        "wind_mwh": 30.0,
        "solar_mwh": 6.0,
        "demand_mwh": 36.0,
        "total_generation_mwh": 36.0,
        "net_position_mwh": 0.0,
        "purchase_mwh": 2.0,
        "sale_mwh": 2.0,
        "purchase_cost_gbp": 160.0,
        "sale_revenue_gbp": 200.0,
        "net_market_cash_flow_gbp": 40.0,
    }
    assert totals == pytest.approx(expected_totals, rel=0, abs=1e-9)