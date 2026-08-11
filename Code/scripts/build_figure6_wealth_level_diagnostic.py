"""Build the superseded exploratory saving-rate-by-wealth-level diagnostic.

The diagnostic reuses the active-saving reconstruction behind Figure 5 but
keeps all 21 fine wealth cohorts. It is not labelled as Figure 6 because the
available denominator is pretax income rather than the paper's disposable-
income concept, and the horizontal coordinate is a cohort mean rather than a
fixed household-level wealth bin.

Use ``build_figure6_authors_data.py`` for the preferred exact-method output.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd

from unveiling.figure5_authors import (
    construct_annual_saving,
    construct_group_wealth,
    load_aggregate_wealth,
    load_fine_wealth_shares,
    load_private_saving,
    load_valuation_inputs,
)
from unveiling.figure6_wealth_level_diagnostic import (
    construct_fine_wealth_profiles,
    load_demographics,
    summarize_wealth_windows,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUTHOR_DATA = PROJECT_ROOT / "MSS2021Febreplicationkit" / "data"
PROCESSED = PROJECT_ROOT / "Data" / "processed"
FIGURES = PROJECT_ROOT / "Results_Proposal" / "figures"

ANNUAL_OUTPUT = PROCESSED / "figure6_wealth_level_profiles.csv"
WINDOW_OUTPUT = PROCESSED / "figure6_wealth_level_windows.csv"
FIGURE_OUTPUT = FIGURES / "figure6_wealth_level_diagnostic.png"

COLORS = {
    "pre_1982": "#6F7D8C",
    "post_1982": "#C85200",
    "baseline_decade": "#6F7D8C",
    "late_decade": "#C85200",
}
LABELS = {
    "pre_1982": "1963–1982",
    "post_1982": "1983–2016",
    "baseline_decade": "1973–1982",
    "late_decade": "2007–2016",
}


def _format_real_dollars(value: float, _position: float) -> str:
    """Format signed real-dollar values compactly on a symlog axis."""

    sign = "−" if value < 0 else ""
    magnitude = abs(value)
    if magnitude >= 1_000_000_000:
        return f"{sign}${magnitude / 1_000_000_000:.0f}bn"
    if magnitude >= 1_000_000:
        return f"{sign}${magnitude / 1_000_000:.0f}m"
    if magnitude >= 1_000:
        return f"{sign}${magnitude / 1_000:.0f}k"
    return f"{sign}${magnitude:.0f}"


def _plot_window_pair(
    axis: plt.Axes,
    windows: pd.DataFrame,
    *,
    window_names: tuple[str, str],
    title: str,
) -> None:
    """Plot two fine-cohort profiles on one wealth-level axis."""

    for window_name in window_names:
        selected = windows.loc[windows["window"] == window_name].sort_values(
            "cohort_order"
        )
        axis.plot(
            selected["real_mean_wealth_per_adult_2018_usd"],
            100 * selected["active_saving_to_pretax_income"],
            color=COLORS[window_name],
            linewidth=2.1,
            marker="o",
            markersize=4.2,
            markeredgecolor="white",
            markeredgewidth=0.5,
            label=LABELS[window_name],
            zorder=3,
        )
    axis.axhline(0, color="#73808C", linewidth=0.8, zorder=1)
    axis.set_xscale("symlog", linthresh=50_000, linscale=1.0)
    axis.set_xlim(-100_000, 1_200_000_000)
    axis.set_xticks(
        [
            -100_000,
            0,
            100_000,
            1_000_000,
            10_000_000,
            100_000_000,
            1_000_000_000,
        ]
    )
    axis.xaxis.set_major_formatter(FuncFormatter(_format_real_dollars))
    axis.set_title(title, color="#12304A", fontweight="bold")
    axis.set_xlabel("Mean net wealth per adult (2018 dollars; symlog scale)")
    axis.grid(axis="y", color="#DCE3E8", linewidth=0.8)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(frameon=False, loc="upper left")


def plot_wealth_level_profiles(
    windows: pd.DataFrame,
    output_path: Path,
) -> None:
    """Plot paper-aligned and endpoint-period wealth-level profiles."""

    figure, axes = plt.subplots(1, 2, figsize=(12.4, 5.1), sharey=True)
    _plot_window_pair(
        axes[0],
        windows,
        window_names=("pre_1982", "post_1982"),
        title="Paper-aligned periods",
    )
    _plot_window_pair(
        axes[1],
        windows,
        window_names=("baseline_decade", "late_decade"),
        title="Endpoint decades",
    )
    axes[0].set_ylabel("Active saving / cohort pretax income (%)")
    axes[1].text(
        0.98,
        0.03,
        "Each marker is one supplied wealth-percentile cohort",
        transform=axes[1].transAxes,
        ha="right",
        va="bottom",
        fontsize=8,
        color="#53616E",
    )
    figure.suptitle(
        "Exploratory saving profiles by wealth level",
        color="#12304A",
        fontsize=14,
        fontweight="bold",
    )
    figure.text(
        0.5,
        0.015,
        "2021 authors-kit inputs · active-saving numerator from the 2025 "
        "identity · repeated cross-sections; this is not an exact Figure 6 "
        "replication",
        ha="center",
        va="bottom",
        fontsize=8,
        color="#53616E",
    )
    figure.tight_layout(rect=(0, 0.07, 1, 0.93), w_pad=2.4)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    """Build the annual data, window summaries, and static diagnostic."""

    aggregate = load_aggregate_wealth(
        AUTHOR_DATA / "finalfiles" / "YwealthFOF.dta"
    )
    fine_shares = load_fine_wealth_shares(
        AUTHOR_DATA / "PSZusdina" / "Yszshares_fine.dta"
    )
    valuations = load_valuation_inputs(
        AUTHOR_DATA / "finalfiles" / "Ywealthreturns.dta"
    )
    annual_saving = construct_annual_saving(
        construct_group_wealth(aggregate, fine_shares),
        valuations,
        load_private_saving(
            AUTHOR_DATA / "finalfiles" / "YinequalityNIPAanalysis.dta"
        ),
    )
    profiles = construct_fine_wealth_profiles(
        aggregate,
        fine_shares,
        valuations,
        annual_saving,
        load_demographics(AUTHOR_DATA / "PSZusdina" / "parameters_mss.csv"),
    )
    windows = summarize_wealth_windows(profiles)

    PROCESSED.mkdir(parents=True, exist_ok=True)
    profiles.to_csv(ANNUAL_OUTPUT, index=False)
    windows.to_csv(WINDOW_OUTPUT, index=False)
    plot_wealth_level_profiles(windows, FIGURE_OUTPUT)

    print("Approach: exploratory active-saving profiles by cohort mean wealth")
    for path in (ANNUAL_OUTPUT, WINDOW_OUTPUT, FIGURE_OUTPUT):
        print(f"Wrote {path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
