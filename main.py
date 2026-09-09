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


def main() -> None:
    """Run our example and print its report."""

    result = calculate_portfolio_period(
        wind_mwh=8.0,
        solar_mwh=2.0,
        demand_mwh=12.0,
        price_gbp_per_mwh=80.0,
    )

    print("POWER PORTFOLIO: ONE HALF-HOUR")
    print(f"Wind generation: {result['wind_mwh']:.2f} MWh")
    print(f"Solar PV generation: {result['solar_mwh']:.2f} MWh")
    print(f"Total generation: {result['total_generation_mwh']:.2f} MWh")
    print(f"Customer consumption: {result['demand_mwh']:.2f} MWh")
    print()
    print(
        "Net position before market trades: "
        f"{result['net_position_mwh']:+.2f} MWh"
    )
    print(f"Position: {result['position']}")
    print(f"Required purchase: {result['purchase_mwh']:.2f} MWh")
    print(f"Required sale: {result['sale_mwh']:.2f} MWh")
    print()
    print(f"Wholesale price: {result['price_gbp_per_mwh']:.2f} GBP/MWh")
    print(f"Wholesale purchase cost: {result['purchase_cost_gbp']:.2f} GBP")
    print(f"Wholesale sale revenue: {result['sale_revenue_gbp']:.2f} GBP")
    print(f"Net market cash flow: {result['net_market_cash_flow_gbp']:+.2f} GBP")


if __name__ == "__main__":
    main()