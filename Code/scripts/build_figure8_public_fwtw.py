"""Build the public-FWTW full-Leontief Figure 8 reconstruction.

This is the newer-public-data robustness route.  It writes only its own
outputs; the three-way comparison is a separate build step.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from unveiling.figure1 import read_fwtw
from unveiling.figure8_public_fwtw import (
    DISPLAY_GROUPS,
    construct_public_fwtw_figure8,
    load_authors_national_income,
    load_distributional_shares,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FWTW_INPUT = PROJECT_ROOT / "Data/raw/fwtw/fwtw_data_2026-06-18.csv"
AUTHOR_DATA = PROJECT_ROOT / "MSS2021Febreplicationkit/data"
PROCESSED = PROJECT_ROOT / "Data/processed"
INTERIM = PROJECT_ROOT / "Data/interim"
FIGURES = PROJECT_ROOT / "Results_Proposal/figures"

PUBLIC_OUTPUT = PROCESSED / "figure8_public_fwtw_full_leontief.csv"
SENSITIVITY_OUTPUT = PROCESSED / "figure8_public_fwtw_clipped_sensitivity.csv"
DIAGNOSTICS_OUTPUT = INTERIM / "figure8_public_fwtw_network_diagnostics.csv"

PUBLIC_FIGURE = FIGURES / "figure8_public_fwtw_full_leontief.png"
SENSITIVITY_FIGURE = FIGURES / "figure8_public_fwtw_sensitivity.png"

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


def main() -> None:
    """Run, validate, and export only the public-FWTW reconstruction."""

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

    PROCESSED.mkdir(parents=True, exist_ok=True)
    INTERIM.mkdir(parents=True, exist_ok=True)
    public.to_csv(PUBLIC_OUTPUT, index=False)
    sensitivity.to_csv(SENSITIVITY_OUTPUT, index=False)
    diagnostics.to_csv(DIAGNOSTICS_OUTPUT, index=False)
    plot_public_result(public, PUBLIC_FIGURE)
    plot_sensitivity(public, sensitivity, SENSITIVITY_FIGURE)

    print("Approach: public-FWTW mixed-vintage full-Leontief reconstruction")
    for path in (
        PUBLIC_OUTPUT,
        SENSITIVITY_OUTPUT,
        DIAGNOSTICS_OUTPUT,
        PUBLIC_FIGURE,
        SENSITIVITY_FIGURE,
    ):
        print(f"Wrote {path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
