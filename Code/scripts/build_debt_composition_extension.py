"""Build the mortgage-versus-consumer-credit research extension.

The script holds the validated 2021 direct-cell/full-Leontief network fixed,
returns its two primary household-debt categories separately, and combines
those stocks with matching write-down-adjusted Figure 5 borrowing flows.
Authors' files are read only; all outputs are project-owned.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from unveiling.debt_composition_extension import (
    construct_debt_saving_components,
    summarize_debt_saving_periods,
)
from unveiling.figure5_authors import (
    construct_group_wealth,
    load_aggregate_wealth,
    load_fine_wealth_shares,
    load_valuation_inputs,
)
from unveiling.figure8_2021_direct import (
    build_debt_composition_panel,
    construct_2021_direct_full_leontief,
    load_2021_direct_cells,
    load_authors_national_income,
    load_distributional_shares,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUTHOR_DATA = PROJECT_ROOT / "MSS2021Febreplicationkit/data"
PROCESSED = PROJECT_ROOT / "Data/processed"
INTERIM = PROJECT_ROOT / "Data/interim"
FIGURES = PROJECT_ROOT / "Results_Proposal/figures"

STOCK_OUTPUT = PROCESSED / "debt_composition_2021_direct.csv"
SAVING_OUTPUT = PROCESSED / "debt_composition_saving_contributions.csv"
PERIOD_OUTPUT = PROCESSED / "debt_composition_period_summary.csv"
HEADLINE_OUTPUT = PROCESSED / "debt_composition_presentation_metrics.csv"
DIAGNOSTICS_OUTPUT = INTERIM / "debt_composition_accounting_diagnostics.csv"
LIABILITY_FIGURE = FIGURES / "debt_composition_liability_stocks.png"
NET_POSITION_FIGURE = FIGURES / "debt_composition_unveiled_net_positions.png"
SAVING_FIGURE = FIGURES / "debt_composition_saving_contributions.png"

GROUPS = ("top_1", "next_9", "next_40", "bottom_50")
COLORS = {
    "top_1": "#C85200",
    "next_9": "#FFBC79",
    "next_40": "#1170AA",
    "bottom_50": "#A3CCE9",
}
LABELS = {
    "top_1": "Top 1%",
    "next_9": "Next 9%",
    "next_40": "Next 40%",
    "bottom_50": "Bottom 50%",
}
CATEGORY_LABELS = {
    "home_mortgage": "Home mortgages",
    "consumer_credit": "Consumer credit",
}


def _category_slice(panel: pd.DataFrame, category: str, group: str) -> pd.DataFrame:
    """Return one sorted category-group series from the validated long panel."""

    output = panel.loc[
        (panel["category"] == category) & (panel["group"] == group)
    ].sort_values("year")
    if output["year"].tolist() != list(range(1963, 2017)):
        raise ValueError(f"incomplete extension series for {category}/{group}")
    return output


def plot_liability_stocks(panel: pd.DataFrame, output_path: Path) -> None:
    """Plot gross debt owed by category and wealth group relative to 1982."""

    figure, axes = plt.subplots(1, 2, figsize=(11.2, 4.4), sharex=True, sharey=True)
    for axis, category in zip(
        axes, ("home_mortgage", "consumer_credit"), strict=True
    ):
        for group in GROUPS:
            series = _category_slice(panel, category, group)
            axis.plot(
                series["year"],
                100 * series["debt_liabilities_relative_to_1982"],
                color=COLORS[group],
                linewidth=2.4 if group in {"top_1", "next_40"} else 1.8,
                label=LABELS[group],
            )
        axis.axhline(0.0, color="#73808C", linewidth=0.8)
        axis.set_title(CATEGORY_LABELS[category])
        axis.set_xlabel("Year")
        axis.grid(axis="y", color="#DCE3E8", linewidth=0.8)
        axis.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel(
        "Percentage points of national income\n(relative to 1982)"
    )
    handles, labels = axes[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="lower center", ncol=4, frameon=False)
    figure.suptitle(
        "Gross household liabilities by debt category and wealth group",
        color="#12304A",
        fontsize=14,
        fontweight="bold",
    )
    figure.text(
        0.99,
        0.01,
        "2021 authors-kit levels and DINA shares · liabilities are positive amounts owed",
        ha="right",
        va="bottom",
        fontsize=8,
        color="#53616E",
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout(rect=(0, 0.10, 1, 0.92))
    figure.savefig(output_path, dpi=240, bbox_inches="tight")
    plt.close(figure)


def plot_unveiled_net_positions(panel: pd.DataFrame, output_path: Path) -> None:
    """Plot category-specific unveiled assets minus liabilities."""

    figure, axes = plt.subplots(1, 2, figsize=(11.2, 4.4), sharex=True, sharey=True)
    for axis, category in zip(
        axes, ("home_mortgage", "consumer_credit"), strict=True
    ):
        for group in GROUPS:
            series = _category_slice(panel, category, group)
            axis.plot(
                series["year"],
                100 * series["net_debt_relative_to_1982"],
                color=COLORS[group],
                linewidth=2.4 if group in {"top_1", "next_40"} else 1.8,
                label=LABELS[group],
            )
        axis.axhline(0.0, color="#73808C", linewidth=0.8)
        axis.set_title(CATEGORY_LABELS[category])
        axis.set_xlabel("Year")
        axis.grid(axis="y", color="#DCE3E8", linewidth=0.8)
        axis.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel(
        "Unveiled assets minus liabilities\n(pp national income, relative to 1982)"
    )
    handles, labels = axes[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="lower center", ncol=4, frameon=False)
    figure.suptitle(
        "Category-specific net positions after the full Leontief unveiling",
        color="#12304A",
        fontsize=14,
        fontweight="bold",
    )
    figure.text(
        0.99,
        0.01,
        "2021 direct cells · eight coarsened intermediaries · positive means net ultimate lender",
        ha="right",
        va="bottom",
        fontsize=8,
        color="#53616E",
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout(rect=(0, 0.10, 1, 0.92))
    figure.savefig(output_path, dpi=240, bbox_inches="tight")
    plt.close(figure)


def plot_saving_contributions(periods: pd.DataFrame, output_path: Path) -> None:
    """Plot 1998--2007 debt contributions to active saving by wealth group."""

    focus = periods.loc[periods["period"] == "1998–2007"].copy()
    pivot = focus.pivot(
        index="group",
        columns="category",
        values="mean_active_saving_contribution_pp_national_income",
    ).loc[list(GROUPS)]
    figure, axis = plt.subplots(figsize=(8.4, 4.6))
    positions = range(len(GROUPS))
    width = 0.36
    axis.bar(
        [position - width / 2 for position in positions],
        pivot["home_mortgage"],
        width,
        label="Home mortgages",
        color="#C85200",
    )
    axis.bar(
        [position + width / 2 for position in positions],
        pivot["consumer_credit"],
        width,
        label="Consumer credit",
        color="#1170AA",
    )
    axis.axhline(0.0, color="#73808C", linewidth=0.8)
    axis.set_xticks(list(positions), [LABELS[group] for group in GROUPS])
    axis.set_ylabel("Average annual contribution\n(pp national income)")
    axis.set_title("Debt contributions to active saving, 1998–2007")
    axis.grid(axis="y", color="#DCE3E8", linewidth=0.8)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(frameon=False, ncol=2, loc="lower left")
    axis.text(
        0.99,
        0.02,
        "Negative values mean active borrowing reduced measured saving",
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


def build_headline_metrics(
    stock_panel: pd.DataFrame,
    period_summary: pd.DataFrame,
) -> pd.DataFrame:
    """Create a tidy, generated metric layer for the short presentation."""

    records: list[dict[str, float | str]] = []
    for year in (2007, 2016):
        selected = stock_panel.loc[
            stock_panel["year"].eq(year)
            & stock_panel["group"].isin(GROUPS)
        ]
        for row in selected.itertuples(index=False):
            records.extend(
                [
                    {
                        "metric": f"liability_change_1982_to_{year}_pp_ni",
                        "category": row.category,
                        "group": row.group,
                        "value": 100.0 * row.debt_liabilities_relative_to_1982,
                    },
                    {
                        "metric": f"net_position_change_1982_to_{year}_pp_ni",
                        "category": row.category,
                        "group": row.group,
                        "value": 100.0 * row.net_debt_relative_to_1982,
                    },
                ]
            )
    focus = period_summary.loc[
        period_summary["period"].eq("1998–2007")
        & period_summary["group"].isin(GROUPS)
    ]
    for row in focus.itertuples(index=False):
        records.append(
            {
                "metric": "mean_active_saving_contribution_1998_2007_pp_ni",
                "category": row.category,
                "group": row.group,
                "value": row.mean_active_saving_contribution_pp_national_income,
            }
        )
    output = pd.DataFrame(records).sort_values(
        ["metric", "category", "group"]
    ).reset_index(drop=True)
    if output.duplicated(["metric", "category", "group"]).any():
        raise ValueError("presentation metrics: duplicate metric-category-group")
    return output


def main() -> None:
    """Build, validate, and export the Stage 1 extension evidence."""

    direct = load_2021_direct_cells(
        AUTHOR_DATA / "finalfiles/Yunveilhhd.dta"
    )
    distributional_shares = load_distributional_shares(
        AUTHOR_DATA / "PSZusdina/Yszshares_fine.dta"
    )
    income = load_authors_national_income(
        AUTHOR_DATA / "finalfiles/YwealthFOF.dta"
    )
    wide, diagnostics, _ = construct_2021_direct_full_leontief(
        direct,
        distributional_shares,
        income,
    )
    stock_panel = build_debt_composition_panel(wide)

    group_wealth = construct_group_wealth(
        load_aggregate_wealth(
            AUTHOR_DATA / "finalfiles/YwealthFOF.dta"
        ),
        load_fine_wealth_shares(
            AUTHOR_DATA / "PSZusdina/Yszshares_fine.dta"
        ),
    )
    saving_components = construct_debt_saving_components(
        group_wealth,
        load_valuation_inputs(
            AUTHOR_DATA / "finalfiles/Ywealthreturns.dta"
        ),
    )
    period_summary = summarize_debt_saving_periods(saving_components)
    headline_metrics = build_headline_metrics(stock_panel, period_summary)

    diagnostic_columns = [
        "year",
        "round_variables_read",
        "spectral_radius",
        "category_primary_asset_sum_max_error",
        "category_liability_sum_max_error_millions",
        "category_additivity_max_error_millions",
        "home_mortgage_unassigned_ultimate_share",
        "consumer_credit_unassigned_ultimate_share",
    ]
    extension_diagnostics = diagnostics[diagnostic_columns].copy()

    PROCESSED.mkdir(parents=True, exist_ok=True)
    INTERIM.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    stock_panel.to_csv(STOCK_OUTPUT, index=False)
    saving_components.to_csv(SAVING_OUTPUT, index=False)
    period_summary.to_csv(PERIOD_OUTPUT, index=False)
    headline_metrics.to_csv(HEADLINE_OUTPUT, index=False)
    extension_diagnostics.to_csv(DIAGNOSTICS_OUTPUT, index=False)
    plot_liability_stocks(stock_panel, LIABILITY_FIGURE)
    plot_unveiled_net_positions(stock_panel, NET_POSITION_FIGURE)
    plot_saving_contributions(period_summary, SAVING_FIGURE)

    print("Approach: two-category debt extension on the 2021 direct-cell network")
    for path in (
        STOCK_OUTPUT,
        SAVING_OUTPUT,
        PERIOD_OUTPUT,
        HEADLINE_OUTPUT,
        DIAGNOSTICS_OUTPUT,
        LIABILITY_FIGURE,
        NET_POSITION_FIGURE,
        SAVING_FIGURE,
    ):
        print(f"Wrote {path.relative_to(PROJECT_ROOT)}")
    print("\n1982–2007 liability-stock changes (pp national income):")
    print(
        headline_metrics.loc[
            headline_metrics["metric"]
            == "liability_change_1982_to_2007_pp_ni"
        ].pivot(index="group", columns="category", values="value").round(3)
    )
    print("\n1998–2007 active-saving contributions (pp national income):")
    print(
        headline_metrics.loc[
            headline_metrics["metric"]
            == "mean_active_saving_contribution_1998_2007_pp_ni"
        ].pivot(index="group", columns="category", values="value").round(3)
    )


if __name__ == "__main__":
    main()
