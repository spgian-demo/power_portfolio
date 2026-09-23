""" Lecture 5.1"""

from datetime import date

from portfolio_day import PortfolioDay
from settlement_periods import settlement_period_label
from sample_data import generate_sample_day

def main() -> None:
    seed = 42
    period_inputs = generate_sample_day(seed=seed)


    # Assign the same three illustrative records to one chosen delivery date.
    portfolio_day = PortfolioDay(
        delivery_date=date(2026, 9, 1),
        period_inputs=period_inputs,
    )

    results = portfolio_day.calculate_results()
    period_numbers = [result["settlement_period"] for result in results]
    # previous versions allowed the model to have less than 48 periods. Now only 48.
    if period_numbers != list(range(1, 49)):
        raise ValueError(
            "This full-day report requires settlement periods 1 to 48 in order."
        )

    totals = portfolio_day.calculate_totals()

    print(f"POWER PORTFOLIO: {portfolio_day.period_count} SETTLEMENT PERIODS")
    print(f"Delivery date: {portfolio_day.delivery_date.isoformat()}")
    print(f"Data seed: {seed}")

    for result in results:
        # PortfolioDay has already checked that this identifier is an integer.
        period_number = int(result["settlement_period"])
        period_label = settlement_period_label(
            portfolio_day.delivery_date, period_number
        )

        print()
        print(f"SETTLEMENT PERIOD {period_number} | {period_label}")
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

    positions = [result["position"] for result in results]
    print()
    print("DAILY INTERPRETATION")
    print(f"Long periods: {positions.count('LONG')}")
    print(f"Short periods: {positions.count('SHORT')}")
    print(f"Balanced periods: {positions.count('BALANCED')}")

    # NEW: Monetary totals divided by traded MWh give volume-weighted prices.
    # Use unrounded totals for the division. Round only the displayed values.
    if totals["purchase_mwh"] > 0.0:
        average_purchase_price = totals["purchase_cost_gbp"] / totals["purchase_mwh"]
        print(
            f"Volume-weighted purchase price: {average_purchase_price:.2f} GBP/MWh"
        )
    else:
        print("Volume-weighted purchase price: N/A (no purchases)")

    if totals["sale_mwh"] > 0.0:
        average_sale_price = totals["sale_revenue_gbp"] / totals["sale_mwh"]
        print(f"Volume-weighted sale price: {average_sale_price:.2f} GBP/MWh")
    else:
        print("Volume-weighted sale price: N/A (no sales)")

if __name__ == "__main__":
    main()