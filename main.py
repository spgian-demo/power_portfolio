""" Lecture 3.1: Calculate and interpret 3 settlement periods """

def calculate_portfolio_period(
    wind_mwh: float,
    solar_mwh: float,
    demand_mwh: float,
    price_gbp_per_mwh: float,
) -> dict[str, float | str]:

    """
    Return positions and wholesale cash flows for one settlement period.
    """

    # All energy quantities refer to the SAME half-hour settlement period.
    total_generation_mwh = wind_mwh + solar_mwh
    net_position_mwh = total_generation_mwh - demand_mwh

    # Calculate the position BEFORE the model's wholesale market trade.
    if net_position_mwh > 0.0:
        position = "LONG"
        purchase_mwh = 0.0
        sale_mwh = net_position_mwh
    elif net_position_mwh < 0.0:
        position = "SHORT"
        purchase_mwh = -net_position_mwh
        sale_mwh = 0.0
    else:
        position = "BALANCED"
        purchase_mwh = 0.0
        sale_mwh = 0.0

    purchase_cost_gbp = purchase_mwh * price_gbp_per_mwh
    sale_revenue_gbp = sale_mwh * price_gbp_per_mwh
    net_market_cash_flow_gbp = sale_revenue_gbp - purchase_cost_gbp

    return {
        "wind_mwh": wind_mwh,
        "solar_mwh": solar_mwh,
        "demand_mwh": demand_mwh,
        "price_gbp_per_mwh": price_gbp_per_mwh,
        "total_generation_mwh": total_generation_mwh,
        "net_position_mwh": net_position_mwh,
        "position": position,
        "purchase_mwh": purchase_mwh,
        "sale_mwh": sale_mwh,
        "purchase_cost_gbp": purchase_cost_gbp,
        "sale_revenue_gbp": sale_revenue_gbp,
        "net_market_cash_flow_gbp": net_market_cash_flow_gbp,
    }

def calculate_portfolio_periods(
    period_inputs: list[dict[str, int | float]],
) -> list[dict[str, float | str]]:
    """
    Apply the existing calculation separately to each supplied period.
    """
    results: list[dict[str, float | str]] = []

    for period in period_inputs:
        result = calculate_portfolio_period(
            wind_mwh=period["wind_mwh"],
            solar_mwh=period["solar_mwh"],
            demand_mwh=period["demand_mwh"],
            price_gbp_per_mwh=period["price_gbp_per_mwh"],
        )
        # Keep the period identifier with the result it belongs to.
        result["settlement_period"] = period["settlement_period"]

        results.append(result)

    return results


def summarise_period_results(
    results: list[dict[str, float | str]],
) -> dict[str, float]:
    """Sum selected results across the supplied periods, not a complete day."""


    totals = {
        "wind_mwh": 0.0,
        "solar_mwh": 0.0,
        "demand_mwh": 0.0,
        "total_generation_mwh": 0.0,
        "net_position_mwh": 0.0,
        "purchase_mwh": 0.0,
        "sale_mwh": 0.0,
        "purchase_cost_gbp": 0.0,
        "sale_revenue_gbp": 0.0,
        "net_market_cash_flow_gbp": 0.0,
    }

    for result in results:
        for field in totals:
            # Select numeric fields from our mixed numeric/text dictionary.
            totals[field] += float(result[field])

    return totals

def main() -> None:
    """Run our example and print its report."""

    period_inputs : list[dict[str,int | float]] = [
        {
            "settlement_period": 25,
            "wind_mwh": 8.0,
            "solar_mwh": 2.0,
            "demand_mwh":12.0,
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
    totals = summarise_period_results(results) #new

    print(f"POWER PORTFOLIO: {len(results)} SETTLEMENT PERIODS")

    for result in results:
        print()
        print(f"SETTLEMENT PERIOD {result['settlement_period']:.0f}")
        print(
            f"Wind: {result['wind_mwh']:.2f} MWh | "
            f"Solar PV: {result['solar_mwh']:.2f} MWh"
        )
        print(
            f"Generation: {result['total_generation_mwh']:.2f} MWh | "
            f"Customer consumption: {result['demand_mwh']:.2f} MWh"
        )
        print(
            f"Position before market trades: {result['position']} "
            f"({result['net_position_mwh']:+.2f} MWh)"
        )
        print(
            f"Required purchase: {result['purchase_mwh']:.2f} MWh | "
            f"Required sale: {result['sale_mwh']:.2f} MWh"
        )
        print(f"Wholesale price: {result['price_gbp_per_mwh']:.2f} GBP/MWh")
        print(
            f"Purchase cost: {result['purchase_cost_gbp']:.2f} GBP | "
            f"Sale revenue: {result['sale_revenue_gbp']:.2f} GBP"
        )
        print(f"Net market cash flow: {result['net_market_cash_flow_gbp']:+.2f} GBP")

    print()
    print(f"TOTALS FOR THESE {len(results)} PERIODS ONLY")
    print(f"Wind generation: {totals['wind_mwh']:.2f} MWh")
    print(f"Solar PV generation: {totals['solar_mwh']:.2f} MWh")
    print(f"Total generation: {totals['total_generation_mwh']:.2f} MWh")
    print(f"Customer consumption: {totals['demand_mwh']:.2f} MWh")
    print(f"Sum of pre-trade net positions: {totals['net_position_mwh']:+.2f} MWh")
    print(f"Total purchases: {totals['purchase_mwh']:.2f} MWh")
    print(f"Total sales: {totals['sale_mwh']:.2f} MWh")
    print(f"Total purchase cost: {totals['purchase_cost_gbp']:.2f} GBP")
    print(f"Total sale revenue: {totals['sale_revenue_gbp']:.2f} GBP")
    print(f"Total net market cash flow: {totals['net_market_cash_flow_gbp']:+.2f} GBP")

if __name__ == "__main__":
    main()