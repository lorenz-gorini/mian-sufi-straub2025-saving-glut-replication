"""Compare the paper with three independently generated Figure 8 routes.

Run the three route-specific entry points first.  This script reads their
stable processed outputs and writes only aligned comparison tables and plots.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from unveiling.figure8_comparison import (
    APPROACH_LABELS,
    build_method_comparison,
    calculate_comparison_metrics,
    calculate_same_vintage_operator_metrics,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED = PROJECT_ROOT / "Data/processed"
FIGURES = PROJECT_ROOT / "Results_Proposal/figures"

PAPER_INPUT = PROCESSED / "figure8_paper_digitized.csv"
PROXY_INPUT = PROCESSED / "figure8_authors_proxy.csv"
DIRECT_INPUT = PROCESSED / "figure8_2021_direct_full_leontief.csv"
PUBLIC_INPUT = PROCESSED / "figure8_public_fwtw_full_leontief.csv"

COMPARISON_OUTPUT = PROCESSED / "figure8_method_comparison.csv"
METRICS_OUTPUT = PROCESSED / "figure8_method_comparison_metrics.csv"
OPERATOR_METRICS_OUTPUT = PROCESSED / "figure8_2021_operator_comparison_metrics.csv"

COMPARISON_FIGURE = FIGURES / "figure8_method_comparison.png"
COMPARISON_TOP1_FIGURE = FIGURES / "figure8_method_comparison_top1.png"
COMPARISON_BOTTOM99_FIGURE = FIGURES / "figure8_method_comparison_bottom99.png"
OPERATOR_FIGURE = FIGURES / "figure8_2021_operator_comparison.png"

GROUP_LABELS = {
    "top_1": "Top 1%",
    "bottom_99": "Bottom 99%",
}
GROUP_COLORS = {
    "top_1": "#C85200",
    "bottom_99": "#1170AA",
}
APPROACH_STYLE = {
    "paper": {"color": "#404B55", "linewidth": 2.8, "linestyle": "-"},
    "authors_kit_seven_round_proxy": {
        "color": "#9AA5B1",
        "linewidth": 1.8,
        "linestyle": "--",
    },
    "authors_kit_direct_full_leontief": {
        "color": "#16827B",
        "linewidth": 2.3,
        "linestyle": "-.",
    },
    "public_fwtw_full_leontief": {
        "color": "#D65F00",
        "linewidth": 2.3,
        "linestyle": "-",
    },
}


def _validate_inputs() -> None:
    """Fail with the exact missing route-specific build commands."""

    missing = [
        path
        for path in (PAPER_INPUT, PROXY_INPUT, DIRECT_INPUT, PUBLIC_INPUT)
        if not path.exists()
    ]
    if missing:
        relative = ", ".join(str(path.relative_to(PROJECT_ROOT)) for path in missing)
        raise FileNotFoundError(
            "Figure 8 comparison inputs are missing: "
            f"{relative}. Run the three route-specific build scripts first."
        )


def plot_method_comparison(comparison: pd.DataFrame, output_path: Path) -> None:
    """Plot the two headline groups for the paper and all three routes."""

    figure, axes = plt.subplots(1, 2, figsize=(11.8, 4.3), sharex=True)
    for axis, group in zip(axes, ("top_1", "bottom_99"), strict=True):
        _plot_group_lines(comparison, axis, group=group)
        axis.set_title(GROUP_LABELS[group])
        axis.set_xlabel("Year")
        axis.grid(axis="y", alpha=0.22)
        axis.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Percentage points of national income\n(relative to 1982)")
    handles, labels = axes[0].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        loc="lower center",
        ncol=2,
        frameon=False,
        fontsize=8.5,
    )
    figure.suptitle(
        "Figure 8: separating the operator experiment from the public-data rerun",
        color="#12304A",
        fontsize=13,
        fontweight="bold",
    )
    figure.tight_layout(rect=(0, 0.16, 1, 0.94))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=240, bbox_inches="tight")
    plt.close(figure)


def plot_method_comparison_group(
    comparison: pd.DataFrame,
    *,
    group: str,
    output_path: Path,
) -> None:
    """Plot one headline group with four clearly labelled lines."""

    figure, axis = plt.subplots(figsize=(6.5, 4.15))
    _plot_group_lines(comparison, axis, group=group)
    axis.set(
        xlabel="Year",
        ylabel="Percentage points of national income\n(relative to 1982)",
        title=GROUP_LABELS[group],
    )
    axis.grid(axis="y", alpha=0.22)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(frameon=False, fontsize=8, loc="best")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(output_path, dpi=240, bbox_inches="tight")
    plt.close(figure)


def _plot_group_lines(comparison, axis, *, group: str) -> None:
    """Add the paper and three route lines to one Matplotlib axis."""

    axis.plot(
        comparison["year"],
        100 * comparison[f"paper_{group}_relative_to_1982"],
        label="2025 paper (digitized)",
        **APPROACH_STYLE["paper"],
    )
    for approach_id in (
        "authors_kit_seven_round_proxy",
        "authors_kit_direct_full_leontief",
        "public_fwtw_full_leontief",
    ):
        axis.plot(
            comparison["year"],
            100 * comparison[f"{approach_id}_{group}_relative_to_1982"],
            label=APPROACH_LABELS[approach_id],
            **APPROACH_STYLE[approach_id],
        )
    axis.axhline(0, color="#73808C", linewidth=0.8)


def plot_same_vintage_operator_comparison(
    comparison: pd.DataFrame,
    output_path: Path,
) -> None:
    """Show the most controlled old-input operator comparison."""

    figure, axes = plt.subplots(1, 2, figsize=(10.8, 4.0), sharex=True)
    for axis, group in zip(axes, ("top_1", "bottom_99"), strict=True):
        axis.plot(
            comparison["year"],
            100
            * comparison[
                f"authors_kit_seven_round_proxy_{group}_relative_to_1982"
            ],
            color="#9AA5B1",
            linewidth=2.0,
            linestyle="--",
            label="2021 seven-round result",
        )
        axis.plot(
            comparison["year"],
            100
            * comparison[
                f"authors_kit_direct_full_leontief_{group}_relative_to_1982"
            ],
            color=GROUP_COLORS[group],
            linewidth=2.5,
            label="2021 direct cells + full Leontief",
        )
        axis.axhline(0, color="#73808C", linewidth=0.8)
        axis.set_title(GROUP_LABELS[group])
        axis.set_xlabel("Year")
        axis.grid(axis="y", alpha=0.22)
        axis.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Percentage points of national income\n(relative to 1982)")
    handles, labels = axes[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="lower center", ncol=2, frameon=False)
    figure.suptitle(
        "Holding the 2021 vintage fixed, the infinite-chain correction is modest",
        color="#12304A",
        fontsize=13,
        fontweight="bold",
    )
    figure.tight_layout(rect=(0, 0.13, 1, 0.93))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=240, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    """Read the route outputs and export the three-way comparison."""

    _validate_inputs()
    paper = pd.read_csv(PAPER_INPUT)
    proxy = pd.read_csv(PROXY_INPUT)
    direct = pd.read_csv(DIRECT_INPUT)
    public = pd.read_csv(PUBLIC_INPUT)
    comparison = build_method_comparison(paper, proxy, direct, public)
    metrics = calculate_comparison_metrics(comparison)
    operator_metrics = calculate_same_vintage_operator_metrics(comparison)

    PROCESSED.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(COMPARISON_OUTPUT, index=False)
    metrics.to_csv(METRICS_OUTPUT, index=False)
    operator_metrics.to_csv(OPERATOR_METRICS_OUTPUT, index=False)
    plot_method_comparison(comparison, COMPARISON_FIGURE)
    plot_method_comparison_group(
        comparison,
        group="top_1",
        output_path=COMPARISON_TOP1_FIGURE,
    )
    plot_method_comparison_group(
        comparison,
        group="bottom_99",
        output_path=COMPARISON_BOTTOM99_FIGURE,
    )
    plot_same_vintage_operator_comparison(comparison, OPERATOR_FIGURE)

    print("Comparison: paper benchmark + three separately generated routes")
    for path in (
        COMPARISON_OUTPUT,
        METRICS_OUTPUT,
        OPERATOR_METRICS_OUTPUT,
        COMPARISON_FIGURE,
        COMPARISON_TOP1_FIGURE,
        COMPARISON_BOTTOM99_FIGURE,
        OPERATOR_FIGURE,
    ):
        print(f"Wrote {path.relative_to(PROJECT_ROOT)}")
    print(
        metrics.loc[metrics["group"].isin(["top_1", "bottom_99"])]
        .drop(columns="approach_id")
        .to_string(index=False)
    )
    print("\nSame-vintage operator comparison:")
    print(
        operator_metrics.loc[
            operator_metrics["group"].isin(["top_1", "bottom_99"])
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
