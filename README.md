# Power Portfolio

Course 121: Power Portfolio Positions and Cash Flows.
Lecture 4.3: Full-Day Code Analysis and Interpretation.

## Current model

The application generates inputs for all 48 half-hour settlement periods
of one ordinary sample day. It compares generation from one wind farm and
one solar PV farm with the electricity consumption of the company's customers.

The date 2026-09-01 is the delivery date. 
The supplied profiles are illustrative inputs.

For each period the model calculates generation, the pre-trade net position,
purchases or sales, and associated wholesale market cash flows. It then adds
those period-level results. 
The same assumed price applies to a period's purchases and sales, with no
transaction fees. No trade execution or bank payment dates are modelled.

## Example data rules

- Wind energy: independent uniform draws between 6 and 14 MWh per period.
- Solar energy: a fixed triangular profile indexed by period start hour,
  with 6 MWh at 12:00 and zero at/before 06:00 and at/after 18:00.
  This directly assigns period energy; it is not an integrated power curve
  or a date-specific daylight calculation.
- For period starts from 07:00 to before 10:00, or 17:00 to before 20:00:
  base demand 15 MWh and base price 110 GBP/MWh.
- For other starts from 06:00 to before 22:00:
  base demand 12 MWh and base price 80 GBP/MWh.
- Otherwise: base demand 9 MWh and base price 60 GBP/MWh.
- Demand adjustments: uniform between -1 and +1 MWh.
- Price adjustments: uniform between -10 and +10 GBP/MWh.
- Inputs are rounded to two decimal places.

All ranges and time blocks are chosen assumptions.

## Reproducibility

`main.py` uses seed 42. `generate_sample_day` creates a fresh local `Random`
instance on every call. Repeat the same code, seed and Python environment to
reproduce the same input records. Changing the seed changes the random wind,
demand and price values, not the fixed solar shape. The same seed is not a guarantee
across edited generation rules or every future Python version.

## Lecture 4.3 additions

The generated input data and the position/cash-flow formulas are unchanged
from Lecture 4.2. Only the reporting script, its existing report test and this
README change.

Before reporting, main.py checks that the calculated period identifiers are
exactly 1 through 48 in order. PortfolioDay still accepts partial days for
earlier examples. This new condition belongs to the full-day report, not the
class. It checks period coverage under the ordinary-day convention, not
clock-change dates or the accuracy of the energy/price inputs.

The report also counts long, short and balanced periods and calculates:

- Volume-weighted purchase price = total purchase cost / total purchases.
- Volume-weighted sale price = total sale revenue / total sales.

These are descriptions of the already calculated transactions. They are not
new prices used to recalculate cash flows, and not a simple average of all
48 wholesale prices. A price is shown as N/A when its traded quantity is zero.
The division uses unrounded computed totals; only display values are rounded.

With seed 42 the reference example has 29 long periods, 19 short periods and
no balanced periods. Generation is 571.81 MWh and consumption is 554.67 MWh.
Purchases total 62.67 MWh and sales total 79.81 MWh. Purchase cost is displayed
as 6085.54 GBP, sale revenue as 5648.26 GBP and net market cash flow as
-437.28 GBP. Volume-weighted purchase and sale prices are 97.10 and 70.77
GBP/MWh respectively, rounded for display.

This illustrates why a positive daily net energy quantity does not imply a
positive market cash flow. Period-level quantities and prices matter. It does
not demonstrate real trading performance, optimal scheduling or company profit.