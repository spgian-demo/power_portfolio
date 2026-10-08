# Power Portfolio Positions and Cash Flows

**A Python model linking electricity quantities to wholesale market cash flows.**

Developed by **Dr. Spyros Giannelos**.

The example company owns one wind farm and one solar PV farm. It also has an obligation to supply electricity to its customers. We analyse these components together as one power portfolio.

We focus on the electricity market of Great Britain, where every day consists of 48 settlement periods. For each half-hour settlement period, the model compares the total electricity generation with the company's customer electricity consumption. It calculates the electricity surplus or shortage for the company, the purchase or sale of electricity required under the model's assumptions, and the associated wholesale electricity market cash flow.

**This is a position-and-cash-flow model. It is not a live trading system or a complete company-profit model.**

## Why this project is useful

The project provides a foundation for power-portfolio analysis, trading support and electricity-supply analysis. It connects generation and consumption data to commercial quantities and monetary results. It also demonstrates a reusable Python calculation, file-based inputs, numerical and visual outputs, automated checks, and Git version history.

## What the completed application does

- Reads one  day's input data from CSV and checks coverage of periods 1 to 48.
- Calculates each period's generation, net position, purchase or sale, and wholesale market cash flow.
- Reports totals and volume-weighted purchase and sale prices.
- Exports a period-results CSV and four separate PNG charts.
- Includes controlled zero-price, negative-price and daily price-sensitivity examples in `price_examples.py`.
- Retains 24 automated test functions in the supplied reference implementation.

## Model conventions

All generation and consumption inputs are **energy quantities in MWh for one half-hour**. They are not instantaneous power values in MW. Do not multiply an input MWh quantity by 0.5 hours again.

For each settlement period:

```text
total_generation_mwh = wind_mwh + solar_mwh
net_position_mwh = total_generation_mwh - demand_mwh
purchase_mwh = max(-net_position_mwh, 0)
sale_mwh = max(net_position_mwh, 0)
purchase_cost_gbp = purchase_mwh * price_gbp_per_mwh
sale_revenue_gbp = sale_mwh * price_gbp_per_mwh
net_market_cash_flow_gbp = sale_revenue_gbp - purchase_cost_gbp
```

The `max` expressions above summarise the existing `if`/`elif`/`else` implementation; they are not a proposed code change.

A positive net position is **long** and a negative position is **short**, measured before the model's wholesale transaction. Purchase and sale quantities are non-negative. The price, purchase-cost value, sale-revenue value and signed cash flow can be negative.

The same assumed wholesale price applies to purchases and sales within a period. The full shortage is purchased or the full surplus is sold, without trading fees. There is no price-responsive change in generation or customer consumption.

Calculate transactions separately for each period, then sum the results. Surpluses in later periods do not remove earlier shortages because this version contains no storage.

## Requirements and running the project

The lessons use PyCharm on a Mac, but the code does not depend on PyCharm. 

`requirements.txt` records the two direct dependencies already used by the project. It is not a complete cross-platform dependency lockfile. No AI subscription or external data-service account is required.

## Input dataset

This is a saved **illustrative** dataset, originally generated with seed 42. It does not contain real company measurements or observed market prices. The date labels the example; it did not determine the generator's weather or seasonal profiles. All prices in this reference dataset are positive.

Keep these six CSV columns in the stated order:

| Column | Meaning |
|---|---|
| `delivery_date` | Delivery date, for example `2026-09-01`. All records must share one date. |
| `settlement_period` | Integer identifier from 1 to 48 for this ordinary-day report. |
| `wind_mwh` | Wind-farm generation during that half-hour. |
| `solar_mwh` | Solar PV generation during that half-hour. |
| `demand_mwh` | Combined customer consumption during that half-hour. |
| `price_gbp_per_mwh` | Assumed wholesale price in pounds per MWh. |

The loader rejects unusable numbers, non-finite values and negative energy inputs. Negative prices remain valid. `PortfolioDay` checks the period identifiers, while `main.py` requires the complete ordered 48-period sequence for its report.

`main.py` reads this file. It does not regenerate or overwrite it. Changing `sample_data.py` alone will therefore not change the CSV-backed report.

## Reference results

These results correspond to the unchanged saved reference input file. Values below are rounded for display.

| Metric | Reference value |
|---|---:|
| Wind generation | 499.81 MWh |
| Solar PV generation | 72.00 MWh |
| Combined generation | 571.81 MWh |
| Customer consumption | 554.67 MWh |
| Sum of pre-trade positions | +17.14 MWh |
| Purchases | 62.67 MWh |
| Sales | 79.81 MWh |
| Wholesale purchase cost | £6,085.54 |
| Wholesale sale revenue | £5,648.26 |
| Net wholesale market cash flow | **-£437.28** |
| Long / short / balanced periods | 29 / 19 / 0 |
| Volume-weighted purchase price | £97.10/MWh |
| Volume-weighted sale price | £70.77/MWh |

Although more MWh are sold than purchased, the volume-weighted purchase price is higher. For these quantities and prices, purchase cost exceeds sale revenue. The net result is a wholesale cash outflow, not a complete company loss.

The largest electricity shortage occurs in period 38: 6.89 MWh. The largest cash outflow instead occurs in period 37: approximately £738.03, because its price is higher. Both quantity and price matter.

## File structure

```text
power_portfolio/
    main.py                       # CSV-backed report, export and plotting
    portfolio_calculations.py     # Period calculations and aggregate totals
    portfolio_day.py              # Dated collection and period checks
    portfolio_io.py               # Input saving, loading and result export
    portfolio_plots.py            # Four separate charts
    settlement_periods.py         # Ordinary-day times and labels
    sample_data.py                # Reproducible illustrative input generator
    price_examples.py             # Controlled price and sensitivity examples
    test_main.py
    test_portfolio_day.py
    test_settlement_periods.py
    requirements.txt
    README.md
    data/                         # Reference input CSV
    outputs/                      # Reference results CSV and four PNGs
    docs/
        course_summary.pptx    # slides with speaker notes
```

## Author

**Dr. Spyros Giannelos**  
**The Energy Data Scientist**


## Collaboration workflow

Review incoming changes before integrating them into your local branch.
Keep reference inputs and financial formulas unchanged unless the task requires it.

## Planned command-line interface

Status: planned, not implemented.

We will add `--input`, `--output-dir` and `--help` so an analyst
can choose files from the terminal without editing Python code.

Existing defaults, input files and financial calculations must
remain unchanged.