# Power Portfolio

Course 121: Power Portfolio Positions and Cash Flows.
Lecture 6.3: Exporting Portfolio Results to CSV.

## Current workflow

Input CSV -> PortfolioDay -> calculations -> printed report and results CSV.

After printing the existing report, main.py exports the same period results to:

    outputs/portfolio_inputs_2026-09-01_results.csv

The outputs folder is created when needed.  

## Inputs

Use these six columns in this order:

    delivery_date,settlement_period,wind_mwh,solar_mwh,demand_mwh,price_gbp_per_mwh


## Git checkpoint and supplied files

Review and stage main.py, portfolio_io.py, test_settlement_periods.py, README.md
and the updated .gitignore. Leave all input CSVs unchanged. Use the existing
branch and this commit message:

    Export period results to a separate CSV

Then push the completed commit. No new branch is required.