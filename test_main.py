import pytest

from main import calculate_portfolio_period

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