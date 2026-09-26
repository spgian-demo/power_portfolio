# Power Portfolio

Course 121: Power Portfolio Positions and Cash Flows.
Lecture 6.2

## Current workflow

CSV file -> restored date and numeric inputs -> PortfolioDay -> existing report.

main.py now reads data/portfolio_inputs_2026-09-01.csv by default. The default
path is relative to main.py, not the terminal's current directory. The delivery
date used by the model comes from the CSV rows, not from the filename.

main.py no longer calls the sample-data generator or saving function. It does
not modify or overwrite the input CSV. A missing file raises an error rather
than silently generating a new dataset. Restore the CSV saved in Lecture 6.1
or use the unchanged reference file supplied in this archive.

## CSV format and scope

Use these six columns in this exact order:

    delivery_date,settlement_period,wind_mwh,solar_mwh,demand_mwh,price_gbp_per_mwh

Use comma separators, a dot for decimal values and ISO date text such as
2026-09-01. Do not put currency symbols or units inside numeric cells.  

All records must have the same delivery date. Numeric inputs must be finite;
energy inputs must be non-negative, while negative prices remain permitted.


## Files changed and Git checkpoint

- portfolio_io.py: add the CSV loading function and the isfinite import.
- main.py: read saved inputs instead of generating and exporting them.
- test_settlement_periods.py: adapt the existing report test for temporary input.
- README.md: explain the workflow and controlled edit.

The reference CSV and all other source files are unchanged from Lecture 6.1.
No new branch is required for this lesson. Review and stage the four files,
run the suite, then use this commit message:

    Load portfolio inputs from CSV without overwriting

Push the checked commit. 