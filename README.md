# Power Portfolio

Course 121: Power Portfolio Positions and Cash Flows.
Lecture 3.2: Refactoring With the PortfolioDay Class.

## Current model

The company owns 1 wind farm and 1 solar PV farm and supplies
customers with electricity. 

The model compares , for every settlement period, the electricity generation and customer
consumption. It calculates the required purchase from the wholesale electricity market,
or sale, and the associated market cash flow.

There are 3 settlement periods in the `PortfolioDay`
object, with delivery date 2026-09-01.  
This code still covers periods 25, 26 and 27 on the delivery
date 1/September/2026.

The 3 financial calculation functions are unchanged 
into `portfolio_calculations.py`.


## Time convention and limitations

The caller must choose an ordinary 24-hour day without a clock change.
Period 1 begins at 00:00. Period 48 ends at 00:00 on the following date.
Start times are inclusive and end times exclusive.

The returned datetimes have no time-zone information. We interpret them as
local clock times, not as UTC timestamps.
This version neither detects clock-change dates nor implements 46- or 50-period
days or time-zone conversion. It must not be used as a general GB settlement
calendar for arbitrary dates.

The helper accepts a date-only object and an integer period number between 1 and
48. 

The existing financial calculations are unchanged.


## Inputs and expected results

| Period | Label | Wind MWh | Solar MWh | Demand MWh | Price GBP/MWh | Position MWh | Market cash flow GBP |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 25 | 12:00-12:30 | 8 | 2 | 12 | 80 | -2 | -160 |
| 26 | 12:30-13:00 | 12 | 2 | 12 | 100 | 2 | 200 |
| 27 | 13:00-13:30 | 10 | 2 | 12 | 60 | 0 | 0 |

Generation and customer consumption each total 36 MWh. The company nevertheless
buys 2 MWh for period 25 and sells 2 MWh for period 26. Purchase cost is 160 GBP.
Sale revenue is 200 GBP. Total net market cash flow remains +40 GBP.
These are three-period totals, not full-day totals or complete company profit.
The model does not choose generation profiles or implement an arbitrage strategy.

## Files

- `portfolio_calculations.py`: the 3 existing calculation functions.
- `portfolio_day.py`: `PortfolioDay`, its date, period checks and calculation methods.
- `main.py`: the input records, object creation and printed report.
- `test_main.py`: the two original tests, with imports updated to the new module.
- `test_portfolio_day.py`: nine tests of the new class, including expected failures.


## Files

- `main.py`: same inputs and report, now with time labels.
- `settlement_periods.py`: new time calculation and label functions.
- `test_settlement_periods.py`: nine new tests, including report-output checks.
- `portfolio_calculations.py`: unchanged financial functions from Lecture 3.2.
- `portfolio_day.py`: unchanged dated collection and period validation.
- `test_main.py`: unchanged two calculation tests.
- `test_portfolio_day.py`: unchanged nine class tests.


## Development checkpoint

Review the changes, run the model and all tests, then stage:

```text
main.py
settlement_periods.py
test_settlement_periods.py
README.md
```

Suggested commit message: `Add settlement-period times and labels`.

Continue on the existing branch and push the completed commit using the workflow
already introduced. Do not commit virtual environments, caches or secrets.
