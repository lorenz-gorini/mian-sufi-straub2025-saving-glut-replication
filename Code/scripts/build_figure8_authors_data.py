"""Build the best-feasible Figure 8 proxy from February 2021 kit data.

The 2025 paper requires completed instrument-level bilateral matrices and an
augmented Leontief solve. Those matrices are not supplied in the 2021 package.
This script therefore uses the kit's fine-cohort seven-round unveiled debt
assets, subtracts fine-cohort debt liabilities, and applies the 2025 Figure 8
normalization. Every output is labelled as a proxy.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from unveiling.figure8_authors import (
    construct_figure8_proxy,
    load_fine_debt_positions,
)
from unveiling.paper_benchmarks import (
    digitize_figure8,
    extract_embedded_figure,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUTHOR_DATA = PROJECT_ROOT / "MSS2021Febreplicationkit" / "data"
PAPER_PDF = PROJECT_ROOT / "MSS_SGR_July242025.pdf"
PROCESSED = PROJECT_ROOT / "Data" / "processed"
FIGURES = PROJECT_ROOT / "Results_Proposal" / "figures"

PROXY_OUTPUT = PROCESSED / "figure8_authors_proxy.csv"
PAPER_OUTPUT = PROCESSED / "figure8_paper_digitized.csv"
COMPARISON_OUTPUT = PROCESSED / "figure8_authors_proxy_comparison.csv"
VALIDATION_OUTPUT = PROCESSED / "figure8_aggregation_validation.csv"
PROXY_FIGURE_OUTPUT = FIGURES / "figure8_authors_proxy.png"
COMPARISON_FIGURE_OUTPUT = FIGURES / "figure8_authors_proxy_comparison.png"

GROUPS = ("top_1", "next_9", "next_40", "bottom_50", "bottom_99")
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


def build_comparison(proxy: pd.DataFrame, paper: pd.DataFrame) -> pd.DataFrame:
    """Align the old-unveiling proxy with the digitized paper through 2016."""

    columns = [
        "year",
        *(f"net_debt_{group}_relative_to_1982" for group in GROUPS),
    ]
    ours = proxy[columns].rename(
        columns={
            f"net_debt_{group}_relative_to_1982": (
                f"proxy_{group}_relative_to_1982"
            )
            for group in GROUPS
        }
    )
    output = paper.merge(ours, on="year", how="inner", validate="one_to_one")
    for group in GROUPS:
        output[f"error_{group}"] = (
            output[f"proxy_{group}_relative_to_1982"]
            - output[f"paper_{group}_relative_to_1982"]
        )
    return output


def plot_proxy(proxy: pd.DataFrame, output_path: Path) -> None:
    """Plot all five net-debt series from the old-unveiling proxy."""

    figure, axis = plt.subplots(figsize=(8.2, 4.7))
    for group in GROUPS:
        main = group in {"top_1", "bottom_99"}
        axis.plot(
            proxy["year"],
            100 * proxy[f"net_debt_{group}_relative_to_1982"],
            color=COLORS[group],
            linewidth=2.6 if main else 1.7,
            linestyle="-" if main else "--",
            label=LABELS[group],
            zorder=3 if main else 2,
        )
    axis.axhline(0, color="#73808C", linewidth=0.8)
    axis.set(
        xlabel="Year",
        ylabel="Percentage points of national income\n(relative to 1982)",
        title="Figure 8 proxy: net household debt by wealth group",
    )
    axis.grid(axis="y", color="#DCE3E8", linewidth=0.8)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(ncol=3, frameon=False, fontsize=9, loc="lower left")
    axis.text(
        0.99,
        0.02,
        "2021 seven-round unveiled positions · 2025 net-debt definition",
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


def plot_comparison(comparison: pd.DataFrame, output_path: Path) -> None:
    """Compare paper and proxy for the top 1% and bottom 99%."""

    figure, axes = plt.subplots(1, 2, figsize=(10.8, 4.1), sharex=True)
    for axis, group in zip(axes, ("top_1", "bottom_99"), strict=True):
        axis.plot(
            comparison["year"],
            100 * comparison[f"paper_{group}_relative_to_1982"],
            color="#8A96A3",
            linewidth=2.7,
            label="2025 paper (digitized)",
        )
        axis.plot(
            comparison["year"],
            100 * comparison[f"proxy_{group}_relative_to_1982"],
            color=COLORS[group],
            linewidth=2.3,
            label="Our 2021-kit proxy",
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
        ncol=2,
        frameon=False,
        fontsize=9,
    )
    figure.suptitle(
        "Figure 8: direction matches; the missing 2025 matrix changes levels",
        color="#12304A",
        fontsize=13,
        fontweight="bold",
    )
    figure.tight_layout(rect=(0, 0.12, 1, 0.94))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    """Run the complete best-feasible Figure 8 proxy build."""

    fine_positions = load_fine_debt_positions(
        AUTHOR_DATA / "finalfiles" / "YinequalityFAanalysis.dta"
    )
    proxy, validation = construct_figure8_proxy(fine_positions)
    with tempfile.TemporaryDirectory(prefix="mss-figure8-") as directory:
        paper_image = extract_embedded_figure(
            PAPER_PDF,
            Path(directory),
            physical_page=29,
            prefix_name="figure8",
        )
        paper = digitize_figure8(paper_image)
    comparison = build_comparison(proxy, paper)

    PROCESSED.mkdir(parents=True, exist_ok=True)
    proxy.to_csv(PROXY_OUTPUT, index=False)
    paper.to_csv(PAPER_OUTPUT, index=False)
    comparison.to_csv(COMPARISON_OUTPUT, index=False)
    validation.to_csv(VALIDATION_OUTPUT, index=False)
    plot_proxy(proxy, PROXY_FIGURE_OUTPUT)
    plot_comparison(comparison, COMPARISON_FIGURE_OUTPUT)

    print("Approach: Figure 8 old-unveiling proxy, not a 2025 matrix rerun")
    for path in (
        PROXY_OUTPUT,
        PAPER_OUTPUT,
        COMPARISON_OUTPUT,
        VALIDATION_OUTPUT,
        PROXY_FIGURE_OUTPUT,
        COMPARISON_FIGURE_OUTPUT,
    ):
        print(f"Wrote {path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
