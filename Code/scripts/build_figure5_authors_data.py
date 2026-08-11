"""Build Figure 5 with 2021 authors-kit inputs and the 2025 method.

The annual calculation starts from supplied Financial Accounts totals, fine
DINA wealth shares, valuation inputs, and national-account private saving. It
then applies the 2025 paper's ten-year trailing mean and 1982 normalization.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from unveiling.figure5_authors import (
    apply_figure5_display,
    build_saving_validation,
    construct_annual_saving,
    construct_group_wealth,
    load_aggregate_wealth,
    load_fine_wealth_shares,
    load_private_saving,
    load_saving_benchmark,
    load_valuation_inputs,
)
from unveiling.paper_benchmarks import (
    digitize_figure5,
    extract_embedded_figure,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUTHOR_DATA = PROJECT_ROOT / "MSS2021Febreplicationkit" / "data"
PAPER_PDF = PROJECT_ROOT / "MSS_SGR_July242025.pdf"
PROCESSED = PROJECT_ROOT / "Data" / "processed"
FIGURES = PROJECT_ROOT / "Results_Proposal" / "figures"

ANNUAL_OUTPUT = PROCESSED / "figure5_authors_annual.csv"
AUTHORS_OUTPUT = PROCESSED / "figure5_authors_data.csv"
PAPER_OUTPUT = PROCESSED / "figure5_paper_digitized.csv"
COMPARISON_OUTPUT = PROCESSED / "figure5_authors_comparison.csv"
VALIDATION_OUTPUT = PROCESSED / "figure5_saving_validation.csv"
RECONSTRUCTION_FIGURE_OUTPUT = (
    FIGURES / "figure5_authors_data_reconstruction.png"
)
COMPARISON_FIGURE_OUTPUT = FIGURES / "figure5_authors_data_comparison.png"

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
    "next_40": "51–90%",
    "bottom_50": "Bottom 50%",
    "bottom_99": "Bottom 99%",
}


def build_comparison(
    authors: pd.DataFrame,
    paper: pd.DataFrame,
) -> pd.DataFrame:
    """Align the reconstructed and digitized Figure 5 series through 2016."""

    columns = ["year", *(f"{group}_relative_to_1982" for group in GROUPS)]
    ours = authors[columns].rename(
        columns={
            f"{group}_relative_to_1982": f"authors_{group}_relative_to_1982"
            for group in GROUPS
        }
    )
    output = paper.merge(ours, on="year", how="inner", validate="one_to_one")
    for group in GROUPS:
        output[f"error_{group}"] = (
            output[f"authors_{group}_relative_to_1982"]
            - output[f"paper_{group}_relative_to_1982"]
        )
    return output


def plot_reconstruction(authors: pd.DataFrame, output_path: Path) -> None:
    """Plot the five reconstructed Figure 5 series."""

    figure, axis = plt.subplots(figsize=(8.2, 4.7))
    for group in GROUPS:
        main = group in {"top_1", "bottom_99"}
        axis.plot(
            authors["year"],
            100 * authors[f"{group}_relative_to_1982"],
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
        title="Figure 5 reconstruction: saving by wealth group",
    )
    axis.grid(axis="y", color="#DCE3E8", linewidth=0.8)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(ncol=3, frameon=False, fontsize=9, loc="lower left")
    axis.text(
        0.99,
        0.02,
        "2021 authors-kit inputs · 2025 saving and display method · 1963–2016",
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
    """Compare the paper and reconstruction for the two headline groups."""

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
            100 * comparison[f"authors_{group}_relative_to_1982"],
            color=COLORS[group],
            linewidth=2.3,
            label="Our authors-data reconstruction",
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
        "Figure 5: same transformation, older data stop in 2016",
        color="#12304A",
        fontsize=13,
        fontweight="bold",
    )
    figure.tight_layout(rect=(0, 0.12, 1, 0.94))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    """Run the complete authors-data Figure 5 reconstruction."""

    aggregate = load_aggregate_wealth(
        AUTHOR_DATA / "finalfiles" / "YwealthFOF.dta"
    )
    fine_shares = load_fine_wealth_shares(
        AUTHOR_DATA / "PSZusdina" / "Yszshares_fine.dta"
    )
    valuations = load_valuation_inputs(
        AUTHOR_DATA / "finalfiles" / "Ywealthreturns.dta"
    )
    private_saving = load_private_saving(
        AUTHOR_DATA / "finalfiles" / "YinequalityNIPAanalysis.dta"
    )
    annual = construct_annual_saving(
        construct_group_wealth(aggregate, fine_shares),
        valuations,
        private_saving,
    )
    authors = apply_figure5_display(annual)
    validation = build_saving_validation(
        annual,
        load_saving_benchmark(
            AUTHOR_DATA / "finalfiles" / "Ysavingwealth.dta"
        ),
    )

    with tempfile.TemporaryDirectory(prefix="mss-figure5-") as directory:
        paper_image = extract_embedded_figure(
            PAPER_PDF,
            Path(directory),
            physical_page=22,
            prefix_name="figure5",
        )
        paper = digitize_figure5(paper_image)
    comparison = build_comparison(authors, paper)

    PROCESSED.mkdir(parents=True, exist_ok=True)
    annual.to_csv(ANNUAL_OUTPUT, index=False)
    authors.to_csv(AUTHORS_OUTPUT, index=False)
    paper.to_csv(PAPER_OUTPUT, index=False)
    comparison.to_csv(COMPARISON_OUTPUT, index=False)
    validation.to_csv(VALIDATION_OUTPUT, index=False)
    plot_reconstruction(authors, RECONSTRUCTION_FIGURE_OUTPUT)
    plot_comparison(comparison, COMPARISON_FIGURE_OUTPUT)

    print("Approach: 2025 Figure 5 method with 2021 authors-kit inputs")
    for path in (
        ANNUAL_OUTPUT,
        AUTHORS_OUTPUT,
        PAPER_OUTPUT,
        COMPARISON_OUTPUT,
        VALIDATION_OUTPUT,
        RECONSTRUCTION_FIGURE_OUTPUT,
        COMPARISON_FIGURE_OUTPUT,
    ):
        print(f"Wrote {path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
