"""Build Figure 8 from 2021 direct cells with the full Leontief operator.

This entry point writes only the third Figure 8 route.  It never reads the
authors' seven-round household-debt allocation and it never rebuilds the
separate public-FWTW route or the cross-method comparison.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from unveiling.figure8_2021_direct import (
    construct_2021_direct_full_leontief,
    load_2021_direct_cells,
    load_authors_national_income,
    load_distributional_shares,
)
from unveiling.figure8_public_fwtw import DISPLAY_GROUPS


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUTHOR_DATA = PROJECT_ROOT / "MSS2021Febreplicationkit/data"
PROCESSED = PROJECT_ROOT / "Data/processed"
INTERIM = PROJECT_ROOT / "Data/interim"
FIGURES = PROJECT_ROOT / "Results_Proposal/figures"

OUTPUT = PROCESSED / "figure8_2021_direct_full_leontief.csv"
DIAGNOSTICS_OUTPUT = INTERIM / "figure8_2021_direct_network_diagnostics.csv"
COMPONENT_OUTPUT = INTERIM / "figure8_2021_direct_component_diagnostics.csv"
FIGURE = FIGURES / "figure8_2021_direct_full_leontief.png"

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


def plot_result(result, output_path: Path) -> None:
    """Plot the 2021-direct-cell full-Leontief net-debt series."""

    figure, axis = plt.subplots(figsize=(8.6, 4.8))
    for group in DISPLAY_GROUPS:
        main = group in {"top_1", "bottom_99"}
        axis.plot(
            result["year"],
            100 * result[f"net_debt_{group}_relative_to_1982"],
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
        title="Figure 8: 2021 direct cells + full Leontief unveiling",
    )
    axis.grid(axis="y", color="#DCE3E8", linewidth=0.8)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(ncol=3, frameon=False, fontsize=9, loc="lower left")
    axis.text(
        0.99,
        0.02,
        "2021-kit completed direct cells · 8 coarsened intermediary blocks · ends 2016",
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


def main() -> None:
    """Run, validate, and export the 2021-direct-cell route."""

    direct = load_2021_direct_cells(
        AUTHOR_DATA / "finalfiles/Yunveilhhd.dta"
    )
    shares = load_distributional_shares(
        AUTHOR_DATA / "PSZusdina/Yszshares_fine.dta"
    )
    income = load_authors_national_income(
        AUTHOR_DATA / "finalfiles/YwealthFOF.dta"
    )
    result, diagnostics, components = construct_2021_direct_full_leontief(
        direct,
        shares,
        income,
    )

    PROCESSED.mkdir(parents=True, exist_ok=True)
    INTERIM.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT, index=False)
    diagnostics.to_csv(DIAGNOSTICS_OUTPUT, index=False)
    components.to_csv(COMPONENT_OUTPUT, index=False)
    plot_result(result, FIGURE)

    print("Approach: 2021 direct-cell vintage + full Leontief")
    print("Seven-round output fields read: 0")
    for path in (OUTPUT, DIAGNOSTICS_OUTPUT, COMPONENT_OUTPUT, FIGURE):
        print(f"Wrote {path.relative_to(PROJECT_ROOT)}")
    headline = result.loc[
        result["year"].isin([2007, 2016]),
        [
            "year",
            "net_debt_top_1_relative_to_1982",
            "net_debt_bottom_99_relative_to_1982",
        ],
    ].copy()
    headline.iloc[:, 1:] *= 100
    print(headline.to_string(index=False))


if __name__ == "__main__":
    main()
