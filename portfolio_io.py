"""Lecture 6.1"""

import csv
from datetime import date
from pathlib import Path


def save_portfolio_inputs_csv(
    file_path: Path,
    delivery_date: date,
    period_inputs: list[dict[str, int | float]],
) -> None:
    """Save one delivery date and its input records in their supplied order.
    """
    fieldnames = [
        "delivery_date",
        "settlement_period",
        "wind_mwh",
        "solar_mwh",
        "demand_mwh",
        "price_gbp_per_mwh",
    ]

    file_path.parent.mkdir(parents=True, exist_ok=True)

    # "w" replaces the existing file; it does not append another day's rows.
    # newline="" lets the csv module handle line endings correctly.
    with file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for period in period_inputs:
            # Repeat the date so each record identifies both date and period.
            writer.writerow(
                {
                    "delivery_date": delivery_date.isoformat(),
                    "settlement_period": period["settlement_period"],
                    "wind_mwh": period["wind_mwh"],
                    "solar_mwh": period["solar_mwh"],
                    "demand_mwh": period["demand_mwh"],
                    "price_gbp_per_mwh": period["price_gbp_per_mwh"],
                }
            )
