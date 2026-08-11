"""Build Figure 6 with 2021 authors-kit inputs and the 2025 method.

The script uses the paper's percentile bins, active-saving numerator, and
personal-plus-corporate disposable-income denominator. It produces the paper's
percentile view and an otherwise identical view indexed by cohort mean real
wealth, allowing the two descriptions to be compared without changing the
saving-rate definition.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from matplotlib.colors import TwoSlopeNorm
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd

# These are shared, validated source-data loaders. No Figure 5 output enters
# the Figure 6 calculation.
from unveiling.figure5_authors import (
    load_aggregate_wealth,
    load_private_saving,
    load_valuation_inputs,
)
from unveiling.figure6_authors import (
    build_paper_comparison,
    build_rolling_profiles,
    construct_annual_percentile_profiles,
    load_demographics,
    load_disposable_income_inputs,
    load_percentile_shares,
    summarize_period_profiles,
)
from unveiling.paper_benchmarks import (
    digitize_figure6,
    extract_embedded_figure,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUTHOR_DATA = PROJECT_ROOT / "MSS2021Febreplicationkit" / "data"
PAPER_PDF = PROJECT_ROOT / "MSS_SGR_July242025.pdf"
INTERIM = PROJECT_ROOT / "Data" / "interim"
PROCESSED = PROJECT_ROOT / "Data" / "processed"
FIGURES = PROJECT_ROOT / "Results_Proposal" / "figures"

PERCENTILE_SHARES = INTERIM / "figure6_percentile_shares.csv"
ANNUAL_OUTPUT = PROCESSED / "figure6_authors_annual.csv"
PERIOD_OUTPUT = PROCESSED / "figure6_authors_data.csv"
PAPER_OUTPUT = PROCESSED / "figure6_paper_digitized.csv"
COMPARISON_OUTPUT = PROCESSED / "figure6_authors_comparison.csv"
ROLLING_OUTPUT = PROCESSED / "figure6_authors_rolling5.csv"
PERCENTILE_FIGURE = FIGURES / "figure6_authors_data_percentiles.png"
WEALTH_FIGURE = FIGURES / "figure6_authors_data_wealth_levels.png"
DUAL_FIGURE = FIGURES / "figure6_percentile_vs_wealth_level.png"
COMPARISON_FIGURE = FIGURES / "figure6_authors_data_comparison.png"
EVOLUTION_FIGURE = FIGURES / "figure6_rolling5_evolution.png"
ROLLING_HEATMAP_FIGURE = FIGURES / "figure6_rolling5_heatmap.png"
ROLLING_SELECTED_FIGURE = FIGURES / "figure6_rolling5_selected_percentiles.png"

COLORS = {
    "pre_1982": "#C85200",
    "post_1982": "#5FA2CE",
}
LABELS = {
    "pre_1982": "1963–1982",
    "post_1982": "1983–2016",
}


def _format_real_dollars(value: float, _position: float) -> str:
    """Format signed real-dollar values compactly."""

    sign = "−" if value < 0 else ""
    magnitude = abs(value)
    if magnitude >= 1_000_000:
        return f"{sign}${magnitude / 1_000_000:.0f}m"
    if magnitude >= 1_000:
        return f"{sign}${magnitude / 1_000:.0f}k"
    return f"{sign}${magnitude:.0f}"


def _plot_percentile_axis(axis: plt.Axes, periods: pd.DataFrame) -> None:
    """Draw the reconstructed paper-percentile view on one axis."""

    for window in ("pre_1982", "post_1982"):
        selected = periods.loc[periods["window"] == window]
        axis.plot(
            selected["percentile_bin"],
            100 * selected["mean_annual_net_saving_rate"],
            color=COLORS[window],
            linewidth=2.5,
            label=LABELS[window],
        )
    axis.axhline(0, color="#73808C", linewidth=0.8)
    axis.set_xlim(39, 101)
    axis.set_xticks([40, 60, 80, 100])
    axis.set_xlabel("Wealth percentile")
    axis.set_ylabel("Net saving rate (%)")
    axis.grid(color="#DCE3E8", linewidth=0.8)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(frameon=False, loc="upper left")


def _wealth_ticks(maximum: float) -> list[float]:
    """Return a compact common tick sequence for the real-wealth view."""

    candidates = [
        -100_000,
        0,
        100_000,
        1_000_000,
        10_000_000,
        100_000_000,
        1_000_000_000,
    ]
    return [tick for tick in candidates if tick <= maximum * 1.05]


def _plot_wealth_axis(axis: plt.Axes, periods: pd.DataFrame) -> None:
    """Draw the same saving rates against mean cohort wealth."""

    maximum = periods["real_mean_wealth_per_adult_2018_usd"].max()
    for window in ("pre_1982", "post_1982"):
        selected = periods.loc[periods["window"] == window]
        axis.plot(
            selected["real_mean_wealth_per_adult_2018_usd"],
            100 * selected["mean_annual_net_saving_rate"],
            color=COLORS[window],
            linewidth=2.5,
            label=LABELS[window],
        )
    axis.axhline(0, color="#73808C", linewidth=0.8)
    axis.set_xscale("symlog", linthresh=50_000, linscale=1.0)
    axis.set_xlim(-100_000, maximum * 1.12)
    axis.set_xticks(_wealth_ticks(maximum))
    axis.xaxis.set_major_formatter(FuncFormatter(_format_real_dollars))
    axis.set_xlabel("Mean net wealth per adult (2018 dollars; symlog scale)")
    axis.set_ylabel("Net saving rate (%)")
    axis.grid(axis="y", color="#DCE3E8", linewidth=0.8)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(frameon=False, loc="upper left")


def _save_single_panel(
    periods: pd.DataFrame,
    output_path: Path,
    *,
    view: str,
) -> None:
    """Save one standalone Figure 6 reconstruction view."""

    figure, axis = plt.subplots(figsize=(8.2, 4.9))
    if view == "percentile":
        _plot_percentile_axis(axis, periods)
        title = "Figure 6 reconstruction: saving rates by wealth percentile"
    elif view == "wealth":
        _plot_wealth_axis(axis, periods)
        title = "Same saving rates, indexed by mean wealth level"
    else:
        raise ValueError(f"unknown Figure 6 view {view!r}")
    axis.set_title(title, color="#12304A", fontweight="bold")
    axis.text(
        0.99,
        0.02,
        "2021 authors-kit inputs · 2025 net-saving-rate definition · "
        "post period ends in 2016",
        transform=axis.transAxes,
        ha="right",
        va="bottom",
        fontsize=8,
        color="#53616E",
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(figure)


def plot_dual_view(periods: pd.DataFrame, output_path: Path) -> None:
    """Place percentile and wealth-level views on a common y-axis."""

    figure, axes = plt.subplots(1, 2, figsize=(12.4, 5.0), sharey=True)
    _plot_percentile_axis(axes[0], periods)
    _plot_wealth_axis(axes[1], periods)
    axes[0].set_title("Paper definition: percentile rank", fontweight="bold")
    axes[1].set_title("Same cohorts: mean wealth level", fontweight="bold")
    axes[1].set_ylabel("")
    figure.suptitle(
        "Figure 6: the denominator and numerator are held fixed",
        color="#12304A",
        fontsize=14,
        fontweight="bold",
    )
    figure.text(
        0.5,
        0.012,
        "Each point has the same net-saving rate in both panels; only the "
        "horizontal coordinate changes · 2021 data end in 2016",
        ha="center",
        fontsize=8,
        color="#53616E",
    )
    figure.tight_layout(rect=(0, 0.06, 1, 0.93), w_pad=2.4)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(figure)


def plot_paper_comparison(
    comparison: pd.DataFrame,
    output_path: Path,
) -> None:
    """Compare digitized paper and old-input reconstruction by period."""

    figure, axes = plt.subplots(1, 2, figsize=(10.8, 4.4), sharex=True, sharey=True)
    for axis, period in zip(
        axes,
        ("pre_1982", "post_1982"),
        strict=True,
    ):
        axis.plot(
            comparison["wealth_percentile"],
            100 * comparison[f"paper_{period}_rate"],
            color="#8A96A3",
            linewidth=2.7,
            label="2025 paper (digitized)",
        )
        axis.plot(
            comparison["wealth_percentile"],
            100 * comparison[f"authors_{period}_rate"],
            color=COLORS[period],
            linewidth=2.3,
            label="Our old-input reconstruction",
        )
        axis.axhline(0, color="#73808C", linewidth=0.8)
        axis.set_title(LABELS[period], fontweight="bold")
        axis.set_xlabel("Wealth percentile")
        axis.set_xticks([40, 60, 80, 100])
        axis.grid(color="#DCE3E8", linewidth=0.8)
        axis.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Net saving rate (%)")
    handles, labels = axes[0].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        loc="lower center",
        ncol=2,
        frameon=False,
    )
    figure.suptitle(
        "Figure 6: exact method, older inputs",
        color="#12304A",
        fontsize=14,
        fontweight="bold",
    )
    figure.tight_layout(rect=(0, 0.12, 1, 0.92), w_pad=2.2)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(figure)


def _rolling_rate_grid(
    rolling_profiles: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return years, percentiles, and percent-valued rolling-rate grid."""

    pivot = rolling_profiles.pivot(
        index="percentile_bin",
        columns="window_end_year",
        values="rolling_mean_net_saving_rate",
    ).sort_index()
    return (
        pivot.columns.to_numpy(),
        pivot.index.to_numpy(),
        100.0 * pivot.to_numpy(),
    )


def _plot_rolling_heatmap_axis(
    axis: plt.Axes,
    rolling_profiles: pd.DataFrame,
) -> object:
    """Plot five-year saving rates across all wealth percentiles."""

    years, percentiles, rates_percent = _rolling_rate_grid(rolling_profiles)
    heatmap = axis.pcolormesh(
        years,
        percentiles,
        rates_percent,
        shading="auto",
        cmap="RdBu_r",
        norm=TwoSlopeNorm(vmin=-20.0, vcenter=0.0, vmax=70.0),
    )
    axis.axvline(1982.5, color="#243748", linewidth=1.1)
    axis.set_xlabel("Five-year window end")
    axis.set_ylabel("Wealth percentile")
    axis.set_yticks([40, 60, 80, 90, 100])
    axis.set_title("The full distribution", fontweight="bold")
    axis.spines[["top", "right"]].set_visible(False)
    return heatmap


def _plot_selected_rolling_axis(
    axis: plt.Axes,
    rolling_profiles: pd.DataFrame,
) -> None:
    """Plot rolling rates for selected upper-tail wealth percentiles."""

    selected_bins = {
        80: ("80th percentile", "#C85200"),
        90: ("90th percentile", "#E59F23"),
        99: ("99th percentile", "#5FA2CE"),
        100: ("Top 1%", "#12304A"),
    }
    for percentile_bin, (label, color) in selected_bins.items():
        selected = rolling_profiles.loc[
            rolling_profiles["percentile_bin"] == percentile_bin
        ]
        axis.plot(
            selected["window_end_year"],
            100.0 * selected["rolling_mean_net_saving_rate"],
            color=color,
            linewidth=2.2,
            label=label,
        )
    axis.axvline(1982.5, color="#73808C", linewidth=1.0)
    axis.axhline(0, color="#73808C", linewidth=0.8)
    axis.set_xlabel("Five-year window end")
    axis.set_ylabel("Five-year mean saving rate (%)")
    axis.set_title("Selected upper-tail cohorts", fontweight="bold")
    axis.grid(color="#DCE3E8", linewidth=0.8)
    axis.legend(frameon=False, loc="upper left", fontsize=9)
    axis.spines[["top", "right"]].set_visible(False)


def _save_rolling_panel(
    rolling_profiles: pd.DataFrame,
    output_path: Path,
    *,
    view: str,
) -> None:
    """Save one presentation-ready five-year Figure 6 panel."""

    figure, axis = plt.subplots(figsize=(8.2, 4.9))
    if view == "heatmap":
        heatmap = _plot_rolling_heatmap_axis(axis, rolling_profiles)
        colorbar = figure.colorbar(heatmap, ax=axis, pad=0.02)
        colorbar.set_label("Five-year mean saving rate (%)")
        title = "Saving rates across the wealth distribution over time"
    elif view == "selected":
        _plot_selected_rolling_axis(axis, rolling_profiles)
        title = "Upper-middle rates fall persistently; the top 1% oscillates"
    else:
        raise ValueError(f"unknown Figure 6 rolling view {view!r}")
    axis.set_title(title, color="#12304A", fontweight="bold")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(figure)


def plot_rolling_evolution(
    rolling_profiles: pd.DataFrame,
    output_path: Path,
) -> None:
    """Show five-year Figure 6 evolution across percentiles and over time."""

    figure, axes = plt.subplots(
        1,
        2,
        figsize=(12.5, 5.0),
        gridspec_kw={"width_ratios": [1.15, 1.0]},
    )
    heatmap = _plot_rolling_heatmap_axis(axes[0], rolling_profiles)
    colorbar = figure.colorbar(heatmap, ax=axes[0], pad=0.02)
    colorbar.set_label("Five-year mean saving rate (%)")
    _plot_selected_rolling_axis(axes[1], rolling_profiles)

    figure.suptitle(
        "Figure 6 evolution: persistent middle decline, volatile top 1%",
        color="#12304A",
        fontsize=14,
        fontweight="bold",
    )
    figure.text(
        0.5,
        0.012,
        "Trailing five-year mean of annual net saving rates · vertical line "
        "marks the 1982/83 split · 2021 authors-kit inputs",
        ha="center",
        fontsize=8,
        color="#53616E",
    )
    figure.tight_layout(rect=(0, 0.06, 1, 0.93), w_pad=2.2)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    """Build the complete old-input Figure 6 reconstruction."""

    aggregate = load_aggregate_wealth(
        AUTHOR_DATA / "finalfiles" / "YwealthFOF.dta"
    )
    valuations = load_valuation_inputs(
        AUTHOR_DATA / "finalfiles" / "Ywealthreturns.dta"
    )
    annual_saving = load_private_saving(
        AUTHOR_DATA / "finalfiles" / "YinequalityNIPAanalysis.dta"
    )
    annual = construct_annual_percentile_profiles(
        aggregate,
        load_percentile_shares(PERCENTILE_SHARES),
        valuations,
        annual_saving,
        load_disposable_income_inputs(
            AUTHOR_DATA / "finalfiles" / "YwealthFOF.dta",
            AUTHOR_DATA / "finalfiles" / "YinequalityNIPAanalysis.dta",
        ),
        load_demographics(AUTHOR_DATA / "PSZusdina" / "parameters_mss.csv"),
    )
    periods = summarize_period_profiles(annual)
    rolling = build_rolling_profiles(annual, window_years=5)

    with tempfile.TemporaryDirectory(prefix="mss-figure6-") as directory:
        paper_image = extract_embedded_figure(
            PAPER_PDF,
            Path(directory),
            physical_page=24,
            prefix_name="figure6",
        )
        paper = digitize_figure6(paper_image)
    comparison = build_paper_comparison(periods, paper)

    PROCESSED.mkdir(parents=True, exist_ok=True)
    annual.to_csv(ANNUAL_OUTPUT, index=False)
    periods.to_csv(PERIOD_OUTPUT, index=False)
    paper.to_csv(PAPER_OUTPUT, index=False)
    comparison.to_csv(COMPARISON_OUTPUT, index=False)
    rolling.to_csv(ROLLING_OUTPUT, index=False)
    _save_single_panel(periods, PERCENTILE_FIGURE, view="percentile")
    _save_single_panel(periods, WEALTH_FIGURE, view="wealth")
    plot_dual_view(periods, DUAL_FIGURE)
    plot_paper_comparison(comparison, COMPARISON_FIGURE)
    plot_rolling_evolution(rolling, EVOLUTION_FIGURE)
    _save_rolling_panel(
        rolling,
        ROLLING_HEATMAP_FIGURE,
        view="heatmap",
    )
    _save_rolling_panel(
        rolling,
        ROLLING_SELECTED_FIGURE,
        view="selected",
    )

    print("Approach: 2025 Figure 6 method with 2021 authors-kit inputs")
    for period in ("pre_1982", "post_1982"):
        error = comparison[f"error_{period}"]
        correlation = np.corrcoef(
            comparison[f"paper_{period}_rate"],
            comparison[f"authors_{period}_rate"],
        )[0, 1]
        print(
            f"{LABELS[period]}: correlation={correlation:.3f}, "
            f"MAE={100 * error.abs().mean():.2f} percentage points"
        )
    for path in (
        ANNUAL_OUTPUT,
        PERIOD_OUTPUT,
        PAPER_OUTPUT,
        COMPARISON_OUTPUT,
        ROLLING_OUTPUT,
        PERCENTILE_FIGURE,
        WEALTH_FIGURE,
        DUAL_FIGURE,
        COMPARISON_FIGURE,
        EVOLUTION_FIGURE,
        ROLLING_HEATMAP_FIGURE,
        ROLLING_SELECTED_FIGURE,
    ):
        print(f"Wrote {path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
