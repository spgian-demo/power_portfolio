""" Lecture 4.1: add time labels to the existing 3-period model"""

from datetime import date

from portfolio_day import PortfolioDay
from settlement_periods import settlement_period_label

def main() -> None:
    """Run 3 periods and print results"""

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


    # Assign the same three illustrative records to one chosen delivery date.
    portfolio_day = PortfolioDay(
        delivery_date=date(2026, 9, 1),
        period_inputs=period_inputs,
    )

    results = portfolio_day.calculate_results()
    totals = portfolio_day.calculate_totals()

    print(f"POWER PORTFOLIO: {portfolio_day.period_count} SETTLEMENT PERIODS")
    print(f"Delivery date: {portfolio_day.delivery_date.isoformat()}")

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

if __name__ == "__main__":
    main()