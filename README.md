# Power Portfolio

Course 121: Power Portfolio Positions and Cash Flows.
Lecture 4.2: Generating Reproducible Example Data.

## Current model

The model generates inputs for all 48 half-hour settlement periods
of the delivery day. It compares generation from one wind farm and
one solar PV farm with the electricity consumption of the company's customers.

The date 2026-09-01 labels the example. The generator does not use the date,
weather, location or installed capacities to construct its profiles.
The supplied profiles are invented inputs, not measurements,
forecasts.

For each period the model calculates generation, the pre-trade net position,
purchases or sales, and associated wholesale market cash flows. It then adds
those period-level results. It does not net electricity across time first.
The same assumed price applies to a period's purchases and sales, with no
transaction fees. No trade execution or bank payment dates are modelled.
Market cash flow is not complete company profit.

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
- Inputs are rounded to two decimal places for teaching convenience.

All ranges and time blocks are chosen assumptions, not industry estimates.
The generated prices are positive; the unchanged financial formulas also
accept negative prices, which will be interpreted in a later lesson.

## Reproducibility

`main.py` uses seed 42. `generate_sample_day` creates a fresh local `Random`
instance on every call. Repeat the same code, seed and Python environment to
reproduce the same input records. Changing the seed changes the random wind,
demand and price values, not the fixed solar shape. Changing only the date
changes labels, not the generated values. The same seed is not a guarantee
across edited generation rules or every future Python version.

The generated list is held in memory during execution. This version does
not save it to a CSV file. Data export is a later course step.
