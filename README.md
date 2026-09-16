# Power Portfolio

Course 121: Power Portfolio Positions and Cash Flows.

## Current version

Lecture 3.1: Code Analysis and Interpretation.

The application analyses three consecutive settlement periods (25, 26 and 27)
from one ordinary sample day. 

The portfolio contains one wind farm, one solar PV farm and the company's
obligation to supply electricity to its customers.

## Calculations

The model calculates generation, customer consumption, the pre-trade net
position, required electricity purchases or sales, and wholesale market cash
flows for each period. It then sums the additive energy and monetary results.

The example requires a 2 MWh purchase at 80 GBP/MWh and a 2 MWh sale at
100 GBP/MWh. The third period is balanced. Total generation and consumption
are both 36 MWh, but transactions are still required in individual periods.
The total net market cash flow is +40 GBP.

## Assumptions and limitations

- Energy inputs are period totals in MWh. Prices are in GBP/MWh.
- One assumed price applies to both buying and selling within each period.
- Market cash flow is not complete company profit or loss.

## Files

- `main.py`: single-period calculation, multi-period processing and reporting.
- `test_main.py`: the original shortage test and a three-period test.
- `.gitignore`: environment and generated-file exclusions from Lecture 2.5.

## Run on macOS

Use the existing project virtual environment from Section 2. No new dependency
is required for Lecture 3.1; pytest was installed in Lecture 2.4.

```bash
./.venv/bin/python main.py
./.venv/bin/python -m pytest -q test_main.py
```
