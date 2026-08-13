"""Build the public-FWTW full-Leontief Figure 8 reconstruction.

This is the new, preferred method reconstruction.  It is separate from
``build_figure8_authors_data.py``, which retains the February 2021 package's
seven-round unveiled positions as an explicitly labelled proxy.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from unveiling.figure1 import read_fwtw
from unveiling.figure8_authors import (
    construct_figure8_proxy,
    load_fine_debt_positions,
)
from unveiling.figure8_public_fwtw import (
    DISPLAY_GROUPS,
    construct_public_fwtw_figure8,
    load_authors_national_income,
    load_distributional_shares,
)
from unveiling.paper_benchmarks import digitize_figure8, extract_embedded_figure


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FWTW_INPUT = PROJECT_ROOT / "Data/raw/fwtw/fwtw_data_2026-06-18.csv"
AUTHOR_DATA = PROJECT_ROOT / "MSS2021Febreplicationkit/data"
PAPER_PDF = PROJECT_ROOT / "MSS_SGR_July242025.pdf"
PROCESSED = PROJECT_ROOT / "Data/processed"
INTERIM = PROJECT_ROOT / "Data/interim"
FIGURES = PROJECT_ROOT / "Results_Proposal/figures"

PUBLIC_OUTPUT = PROCESSED / "figure8_public_fwtw_full_leontief.csv"
SENSITIVITY_OUTPUT = PROCESSED / "figure8_public_fwtw_clipped_sensitivity.csv"
DIAGNOSTICS_OUTPUT = INTERIM / "figure8_public_fwtw_network_diagnostics.csv"
COMPARISON_OUTPUT = PROCESSED / "figure8_method_comparison.csv"
METRICS_OUTPUT = PROCESSED / "figure8_method_comparison_metrics.csv"

PUBLIC_FIGURE = FIGURES / "figure8_public_fwtw_full_leontief.png"
SENSITIVITY_FIGURE = FIGURES / "figure8_public_fwtw_sensitivity.png"
COMPARISON_FIGURE = FIGURES / "figure8_method_comparison.png"
COMPARISON_TOP1_FIGURE = FIGURES / "figure8_method_comparison_top1.png"
COMPARISON_BOTTOM99_FIGURE = FIGURES / "figure8_method_comparison_bottom99.png"

COLORS = {
    "top_1": "#C85200",
    "next_9": "#FFBC79",
    "next_40": "#C8D0D9",
    "bottom_50": "#A3CCE9",
    "bottom_99": "#1170AA",
}
LABELS = {
    "top_1": "Top 1%",
    "next_9": "Next 9%",
    "next_40": "Next 40%",
    "bottom_50": "Bottom 50%",
    "bottom_99": "Bottom 99%",
}


def build_method_comparison(
    public: pd.DataFrame,
    proxy: pd.DataFrame,
    paper: pd.DataFrame,
) -> pd.DataFrame:
    """Align the 2025 paper, full-Leontief rerun, and old seven-round proxy."""

    public_columns = {
        f"net_debt_{group}_relative_to_1982": (
            f"public_fwtw_full_leontief_{group}_relative_to_1982"
        )
        for group in DISPLAY_GROUPS
    }
    proxy_columns = {
        f"net_debt_{group}_relative_to_1982": (
            f"authors_kit_seven_round_proxy_{group}_relative_to_1982"
        )
        for group in DISPLAY_GROUPS
    }
    comparison = paper.merge(
        public[["year", *public_columns]].rename(columns=public_columns),
        on="year",
        how="inner",
        validate="one_to_one",
    ).merge(
        proxy[["year", *proxy_columns]].rename(columns=proxy_columns),
        on="year",
        how="inner",
        validate="one_to_one",
    )
    for group in DISPLAY_GROUPS:
        paper_column = f"paper_{group}_relative_to_1982"
        public_column = f"public_fwtw_full_leontief_{group}_relative_to_1982"
        proxy_column = f"authors_kit_seven_round_proxy_{group}_relative_to_1982"
        comparison[f"public_fwtw_error_{group}"] = (
            comparison[public_column] - comparison[paper_column]
        )
        comparison[f"seven_round_proxy_error_{group}"] = (
            comparison[proxy_column] - comparison[paper_column]
        )
    return comparison


def calculate_comparison_metrics(comparison: pd.DataFrame) -> pd.DataFrame:
    """Calculate correlations and mean absolute errors against the paper."""

    records: list[dict[str, float | str]] = []
    approaches = {
        "public_fwtw_full_leontief": "Public FWTW + full Leontief",
        "authors_kit_seven_round_proxy": "2021 kit + seven-round proxy",
    }
    for prefix, label in approaches.items():
        for group in DISPLAY_GROUPS:
            paper_column = f"paper_{group}_relative_to_1982"
            estimate_column = f"{prefix}_{group}_relative_to_1982"
            error = comparison[estimate_column] - comparison[paper_column]
            records.append(
                {
                    "approach": label,
                    "group": group,
                    "correlation": comparison[[paper_column, estimate_column]]
                    .corr()
                    .iloc[0, 1],
                    "mean_absolute_error_percentage_points": 100 * error.abs().mean(),
                    "root_mean_squared_error_percentage_points": (
                        100 * (error.pow(2).mean() ** 0.5)
                    ),
                }
            )
    return pd.DataFrame(records)


def plot_public_result(public: pd.DataFrame, output_path: Path) -> None:
    """Plot the five public-FWTW full-Leontief net-debt series."""

    figure, axis = plt.subplots(figsize=(8.6, 4.8))
    for group in DISPLAY_GROUPS:
        main = group in {"top_1", "bottom_99"}
        axis.plot(
            public["year"],
            100 * public[f"net_debt_{group}_relative_to_1982"],
            color=COLORS[group],
            linewidth=2.7 if main else 1.7,
            linestyle="-" if main else "--",
            label=LABELS[group],
            zorder=3 if main else 2,
        )
    axis.axhline(0, color="#73808C", linewidth=0.8)
    axis.set(
        xlabel="Year",
        ylabel="Percentage points of national income\n(relative to 1982)",
        title="Figure 8 reconstruction: public FWTW + full Leontief unveiling",
    )
    axis.grid(axis="y", color="#DCE3E8", linewidth=0.8)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(ncol=3, frameon=False, fontsize=9, loc="lower left")
    axis.text(
        0.99,
        0.02,
        "June 2026 FWTW vintage · 2021 DINA/NIPA · sample ends 2016",
        transform=axis.transAxes,
        ha="right",
        va="bottom",
        fontsize=8,
        color="#53616E",
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(output_path, dpi=240, bbox_inches="tight")
    plt.close(figure)


def plot_sensitivity(
    public: pd.DataFrame,
    clipped: pd.DataFrame,
    output_path: Path,
) -> None:
    """Compare reoriented and zero-clipped FWTW treatments."""

    figure, axes = plt.subplots(1, 2, figsize=(10.7, 4.0), sharex=True)
    for axis, group in zip(axes, ("top_1", "bottom_99"), strict=True):
        axis.plot(
            public["year"],
            100 * public[f"net_debt_{group}_relative_to_1982"],
            color=COLORS[group],
            linewidth=2.5,
            label="Negative positions reoriented",
        )
        axis.plot(
            clipped["year"],
            100 * clipped[f"net_debt_{group}_relative_to_1982"],
            color="#8A96A3",
            linewidth=1.9,
            linestyle="--",
            label="Negative cells clipped",
        )
        axis.axhline(0, color="#73808C", linewidth=0.8)
        axis.set_title(LABELS[group])
        axis.set_xlabel("Year")
        axis.grid(axis="y", alpha=0.22)
        axis.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Percentage points of national income\n(relative to 1982)")
    handles, labels = axes[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="lower center", ncol=2, frameon=False)
    figure.suptitle(
        "Reorienting negative FWTW positions is the baseline; "
        "clipping is a sensitivity",
        color="#12304A",
        fontsize=13,
        fontweight="bold",
    )
    figure.tight_layout(rect=(0, 0.12, 1, 0.94))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=240, bbox_inches="tight")
    plt.close(figure)


def plot_method_comparison(comparison: pd.DataFrame, output_path: Path) -> None:
    """Compare the paper with the new and retained Figure 8 approaches."""

    figure, axes = plt.subplots(1, 2, figsize=(11.2, 4.15), sharex=True)
    for axis, group in zip(axes, ("top_1", "bottom_99"), strict=True):
        axis.plot(
            comparison["year"],
            100 * comparison[f"paper_{group}_relative_to_1982"],
            color="#4E5965",
            linewidth=2.8,
            label="2025 paper (digitized)",
        )
        axis.plot(
            comparison["year"],
            100
            * comparison[
                f"public_fwtw_full_leontief_{group}_relative_to_1982"
            ],
            color=COLORS[group],
            linewidth=2.5,
            label="Public FWTW + full Leontief",
        )
        axis.plot(
            comparison["year"],
            100
            * comparison[
                f"authors_kit_seven_round_proxy_{group}_relative_to_1982"
            ],
            color="#8A96A3",
            linewidth=1.9,
            linestyle="--",
            label="2021 kit + seven-round proxy",
        )
        axis.axhline(0, color="#73808C", linewidth=0.8)
        axis.set_title(LABELS[group])
        axis.set_xlabel("Year")
        axis.grid(axis="y", alpha=0.22)
        axis.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Percentage points of national income\n(relative to 1982)")
    handles, labels = axes[0].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        loc="lower center",
        ncol=3,
        frameon=False,
        fontsize=9,
    )
    figure.suptitle(
        "Figure 8: the full operator is new; the public input vintage also changes",
        color="#12304A",
        fontsize=13,
        fontweight="bold",
    )
    figure.tight_layout(rect=(0, 0.14, 1, 0.94))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=240, bbox_inches="tight")
    plt.close(figure)


def plot_method_comparison_group(
    comparison: pd.DataFrame,
    *,
    group: str,
    output_path: Path,
) -> None:
    """Plot one wealth group for legible side-by-side presentation use."""

    figure, axis = plt.subplots(figsize=(6.2, 4.0))
    axis.plot(
        comparison["year"],
        100 * comparison[f"paper_{group}_relative_to_1982"],
        color="#4E5965",
        linewidth=2.8,
        label="2025 paper (digitized)",
    )
    axis.plot(
        comparison["year"],
        100
        * comparison[f"public_fwtw_full_leontief_{group}_relative_to_1982"],
        color=COLORS[group],
        linewidth=2.5,
        label="Public FWTW + full Leontief",
    )
    axis.plot(
        comparison["year"],
        100
        * comparison[
            f"authors_kit_seven_round_proxy_{group}_relative_to_1982"
        ],
        color="#8A96A3",
        linewidth=1.9,
        linestyle="--",
        label="2021 kit + seven-round proxy",
    )
    axis.axhline(0, color="#73808C", linewidth=0.8)
    axis.set(
        xlabel="Year",
        ylabel="Percentage points of national income\n(relative to 1982)",
        title=LABELS[group],
    )
    axis.grid(axis="y", alpha=0.22)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(frameon=False, fontsize=8, loc="best")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(output_path, dpi=240, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    """Run, validate, compare, and export the public-FWTW reconstruction."""

    fwtw = read_fwtw(FWTW_INPUT)
    shares = load_distributional_shares(
        AUTHOR_DATA / "PSZusdina/Yszshares_fine.dta"
    )
    national_income = load_authors_national_income(
        AUTHOR_DATA / "finalfiles/YwealthFOF.dta"
    )
    public, sensitivity, diagnostics = construct_public_fwtw_figure8(
        fwtw,
        shares,
        national_income,
    )

    fine_positions = load_fine_debt_positions(
        AUTHOR_DATA / "finalfiles/YinequalityFAanalysis.dta"
    )
    proxy, _ = construct_figure8_proxy(fine_positions)
    with tempfile.TemporaryDirectory(prefix="mss-figure8-public-") as directory:
        paper_image = extract_embedded_figure(
            PAPER_PDF,
            Path(directory),
            physical_page=29,
            prefix_name="figure8",
        )
        paper = digitize_figure8(paper_image)
    comparison = build_method_comparison(public, proxy, paper)
    metrics = calculate_comparison_metrics(comparison)

    PROCESSED.mkdir(parents=True, exist_ok=True)
    INTERIM.mkdir(parents=True, exist_ok=True)
    public.to_csv(PUBLIC_OUTPUT, index=False)
    sensitivity.to_csv(SENSITIVITY_OUTPUT, index=False)
    diagnostics.to_csv(DIAGNOSTICS_OUTPUT, index=False)
    comparison.to_csv(COMPARISON_OUTPUT, index=False)
    metrics.to_csv(METRICS_OUTPUT, index=False)
    plot_public_result(public, PUBLIC_FIGURE)
    plot_sensitivity(public, sensitivity, SENSITIVITY_FIGURE)
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

    print("Approach: public-FWTW mixed-vintage full-Leontief reconstruction")
    for path in (
        PUBLIC_OUTPUT,
        SENSITIVITY_OUTPUT,
        DIAGNOSTICS_OUTPUT,
        COMPARISON_OUTPUT,
        METRICS_OUTPUT,
        PUBLIC_FIGURE,
        SENSITIVITY_FIGURE,
        COMPARISON_FIGURE,
        COMPARISON_TOP1_FIGURE,
        COMPARISON_BOTTOM99_FIGURE,
    ):
        print(f"Wrote {path.relative_to(PROJECT_ROOT)}")
    headline = metrics.loc[
        metrics["group"].isin(["top_1", "bottom_99"])
    ]
    print(headline.to_string(index=False))


if __name__ == "__main__":
    main()
