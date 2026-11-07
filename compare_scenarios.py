"""Compare the daily totals of a baseline input CSV and a scenario input CSV."""

import argparse
import csv
from datetime import date
from pathlib import Path

from portfolio_day import PortfolioDay
from portfolio_io import load_portfolio_inputs_csv

# The ten daily totals from PortfolioDay.calculate_totals(), in display order.
# Each entry is (totals key, metric label, unit).
METRICS = [
    ("wind_mwh", "Wind generation", "MWh"),
    ("solar_mwh", "Solar PV generation", "MWh"),
    ("total_generation_mwh", "Total electricity generation", "MWh"),
    ("demand_mwh", "Customer electricity demand", "MWh"),
    ("net_position_mwh", "Sum of pre-trade net positions", "MWh"),
    ("purchase_mwh", "Electricity purchased from the market", "MWh"),
    ("sale_mwh", "Electricity sold to the market", "MWh"),
    ("purchase_cost_gbp", "Cost of market purchases", "GBP"),
    ("sale_revenue_gbp", "Revenue from market sales", "GBP"),
    ("net_market_cash_flow_gbp", "Net market cash flow", "GBP"),
]

COMPARISON_COLUMNS = [
    "delivery_date",
    "baseline_file",
    "scenario_file",
    "metric",
    "unit",
    "baseline",
    "scenario",
    "difference",
]


def load_checked_day(csv_path: Path) -> PortfolioDay:
    """Read one input CSV and require settlement periods 1 to 48 in order."""
    try:
        delivery_date, period_inputs = load_portfolio_inputs_csv(csv_path)
        portfolio_day = PortfolioDay(
            delivery_date=delivery_date,
            period_inputs=period_inputs,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{csv_path}: {exc}") from exc

    # PortfolioDay rejects duplicates and decreasing order; this also
    # requires every period from 1 to 48 to be present.
    period_numbers = [period["settlement_period"] for period in period_inputs]
    if period_numbers != list(range(1, 49)):
        raise ValueError(
            f"{csv_path}: settlement periods must be 1 to 48, "
            "in increasing order, each appearing once."
        )

    return portfolio_day


def compare_totals(
    baseline_day: PortfolioDay,
    scenario_day: PortfolioDay,
) -> list[dict[str, float | str]]:
    """Return one row per metric with difference = scenario minus baseline."""
    baseline_totals = baseline_day.calculate_totals()
    scenario_totals = scenario_day.calculate_totals()

    rows: list[dict[str, float | str]] = []
    for key, label, unit in METRICS:
        baseline_value = baseline_totals[key]
        scenario_value = scenario_totals[key]
        rows.append(
            {
                "metric": label,
                "unit": unit,
                "baseline": baseline_value,
                "scenario": scenario_value,
                # Keep the sign: a negative difference is a decrease.
                "difference": scenario_value - baseline_value,
            }
        )
    return rows


def check_output_path(output_csv: Path, input_paths: list[Path]) -> None:
    """Stop if the comparison CSV would replace an input file or a folder."""
    if output_csv.is_dir():
        raise ValueError(f"Output must be a CSV filename, not a folder: {output_csv}")

    for input_path in input_paths:
        same_path = output_csv.resolve() == input_path.resolve()
        # samefile() also catches links and other spellings of the same file.
        if same_path or (output_csv.exists() and output_csv.samefile(input_path)):
            raise ValueError(
                f"Output CSV must not overwrite an input file: {output_csv}"
            )


def save_comparison_csv(
    output_csv: Path,
    delivery_date: date,
    baseline_file: Path,
    scenario_file: Path,
    rows: list[dict[str, float | str]],
) -> None:
    """Save the comparison rows without rounding their values."""
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    with output_csv.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=COMPARISON_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "delivery_date": delivery_date.isoformat(),
                    "baseline_file": str(baseline_file),
                    "scenario_file": str(scenario_file),
                    **row,
                }
            )


def print_comparison_table(rows: list[dict[str, float | str]]) -> None:
    """Print the comparison, rounding numbers to two decimals for display only."""
    header = (
        f"{'Metric':<38} {'Unit':<4} "
        f"{'Baseline':>12} {'Scenario':>12} {'Difference':>12}"
    )
    print(header)
    print("-" * len(header))
    for row in rows:
        print(
            f"{row['metric']:<38} {row['unit']:<4} "
            f"{row['baseline']:>12.2f} {row['scenario']:>12.2f} "
            f"{row['difference']:>+12.2f}"
        )


def run_cli(argv: list[str] | None = None) -> None:
    """Parse command-line options, then compare the baseline and scenario."""
    parser = argparse.ArgumentParser(
        description=(
            "Compare the daily totals of a baseline and a scenario input CSV "
            "(difference = scenario minus baseline)."
        )
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        required=True,
        metavar="CSV",
        help="Existing input CSV for the baseline case.",
    )
    parser.add_argument(
        "--scenario",
        type=Path,
        required=True,
        metavar="CSV",
        help="Existing input CSV for the alternative scenario.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        metavar="CSV",
        help=(
            "Comparison CSV filename, including its folder (default: "
            "outputs/scenario_comparison.csv relative to compare_scenarios.py)."
        ),
    )
    args = parser.parse_args(argv)

    for option, path in (("Baseline", args.baseline), ("Scenario", args.scenario)):
        if not path.is_file():
            parser.error(f"{option} CSV is not an existing file: {path}")

    output_csv = args.output

    if output_csv is None:
        output_csv = (
            Path(__file__).resolve().parent / "outputs" / "scenario_comparison.csv"
        )

    try:
        baseline_day = load_checked_day(args.baseline)
        scenario_day = load_checked_day(args.scenario)

        if baseline_day.delivery_date != scenario_day.delivery_date:
            raise ValueError(
                "Baseline and scenario must have the same delivery date: "
                f"{baseline_day.delivery_date.isoformat()} vs "
                f"{scenario_day.delivery_date.isoformat()}."
            )

        check_output_path(output_csv, [args.baseline, args.scenario])

    except ValueError as exc:
        parser.error(str(exc))

    rows = compare_totals(baseline_day, scenario_day)

    print("SCENARIO COMPARISON")
    print(f"Delivery date: {baseline_day.delivery_date.isoformat()}")
    print(f"Baseline CSV: {args.baseline}")
    print(f"Scenario CSV: {args.scenario}")
    print()
    print_comparison_table(rows)

    save_comparison_csv(
        output_csv=output_csv,
        delivery_date=baseline_day.delivery_date,
        baseline_file=args.baseline,
        scenario_file=args.scenario,
        rows=rows,
    )
    print()
    print(f"Saved {len(rows)} comparison records to: {output_csv}")

if __name__ == "__main__":
    run_cli()