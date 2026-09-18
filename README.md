# Power Portfolio

Course 121: Power Portfolio Positions and Cash Flows.
Lecture 3.2: Refactoring With the PortfolioDay Class.

## Current model

The company owns 1 wind farm and 1 solar PV farm and supplies
customers with electricity. 

The model compares , for every settlement period, the electricity generation and customer
consumption. It calculates the required purchase from the wholesal electricity market,
or sale, and the associated market cash flow.

This version organises 3 illustrative settlement periods in a `PortfolioDay`
object with delivery date **2026-09-01**, as an example. 

The 3 financial calculation functions are moved unchanged from Lecture 3.1
into `portfolio_calculations.py`. The class reuses them.

## Inputs and expected results

| Period | Wind MWh | Solar MWh | Customer consumption MWh | Price GBP/MWh | Net position MWh | Net market cash flow GBP |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 25 | 8 | 2 | 12 | 80 | -2 | -160 |
| 26 | 12 | 2 | 12 | 100 | 2 | 200 |
| 27 | 10 | 2 | 12 | 60 | 0 | 0 |

Across these 3 periods, generation and customer consumption both total
36 MWh. The model nevertheless purchases 2 MWh in period 25 and sells 2 MWh in
period 26. The purchase cost is 160 GBP and the sale revenue is 200 GBP. The total
net market cash flow is therefore +40 GBP. These are not full-day totals or
complete company profit.

## Files

- `portfolio_calculations.py`: the 3 existing calculation functions.
- `portfolio_day.py`: `PortfolioDay`, its date, period checks and calculation methods.
- `main.py`: the input records, object creation and printed report.
- `test_main.py`: the two original tests, with imports updated to the new module.
- `test_portfolio_day.py`: nine tests of the new class, including expected failures.

Keep your existing `.gitignore`. Do not commit `.venv`, caches or secrets.

There are no new third-party dependencies. `datetime` is in Python's standard
library. `pytest` was installed in Lecture 2.4. 
