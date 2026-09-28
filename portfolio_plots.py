"""Lecture 7.1"""

from datetime import date
from pathlib import Path
import matplotlib.pyplot as plt

def save_generation_demand_chart(
    file_path: Path,
    delivery_date: date,
    results: list[dict[str, float | str]],
) -> None:
    """Save one chart of period energy totals, not instantaneous power.
    """
    period_numbers = [result["settlement_period"] for result in results]
    if period_numbers != list(range(1, 49)):
        raise ValueError("This chart requires settlement periods 1 to 48 in order.")

    # 49 boundaries enclose 48 half-hours: 0, 0.5, ..., 23.5, 24.
    # These x-coordinates are hours after midnight on our ordinary sample day.
    edges = [number * 0.5 for number in range(49)] # [0, 0.5, 1, 1.5, 2 ,... 23.5, 24] , range49=0,1,...,48
    # these represent hours after midnight

    wind = [float(result["wind_mwh"]) for result in results]
    solar = [float(result["solar_mwh"]) for result in results]
    generation = [float(result["total_generation_mwh"]) for result in results]
    consumption = [float(result["demand_mwh"]) for result in results]

    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.stairs(wind, edges, baseline=None, label="Wind generation")
    ax.stairs(solar, edges, baseline=None, label="Solar PV generation")
    ax.stairs(
        generation, edges, baseline=None,
        label="Combined generation", linewidth=2.2,
    )
    ax.stairs(
        consumption, edges, baseline=None,
        label="Customer consumption", linewidth=2.2, linestyle="--",
    )

    ax.set_title(
        "Electricity generation and customer consumption\n"
        f"{delivery_date.isoformat()} | Illustrative data"
    )
    ax.set_xlabel("Local clock time (ordinary 48-period day)")
    ax.set_ylabel("Energy in each half-hour (MWh)")
    ax.set_xlim(0, 24)
    ax.margins(y=0.20)
    ax.set_ylim(bottom=0)

    tick_hours = list(range(0, 25, 3))
    tick_labels = [f"{hour:02d}:00" for hour in tick_hours]
    tick_labels[-1] = "00:00\n(+1 day)"
    ax.set_xticks(tick_hours, labels=tick_labels)
    ax.legend(loc="upper left", ncols=2)
    ax.grid(axis="y", alpha=0.25)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fig.savefig(file_path, dpi=160, bbox_inches="tight")
    finally:
        plt.close(fig)