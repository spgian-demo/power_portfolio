# Power Portfolio

Course 121: Power Portfolio Positions and Cash Flows.

## Current model

The application analyses one half-hour settlement period.
It compares electricity generation from one wind farm and one
solar PV farm with the company's customer electricity consumption.

It calculates the net electricity position, required purchases
or sales, and associated wholesale market cash flows.

The inputs are illustrative values, not real company measurements.
The market cash flows are not the company's complete profit or loss.

## Files

- main.py: the calculation function and example report.
- test_main.py: an automated test of the shortage example.

## Running the code

Run the example report:

```bash
python main.py
```

Run the test:

```bash
python -m pytest -q test_main.py
```
