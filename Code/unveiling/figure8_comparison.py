"""Align and evaluate the three deliberately separate Figure 8 routes."""

from __future__ import annotations

import pandas as pd

from .figure8_public_fwtw import DISPLAY_GROUPS


APPROACH_LABELS = {
    "authors_kit_seven_round_proxy": "2021 kit + seven-round proxy",
    "authors_kit_direct_full_leontief": "2021 direct cells + full Leontief",
    "public_fwtw_full_leontief": "Public FWTW + full Leontief",
}


def build_method_comparison(
    paper: pd.DataFrame,
    seven_round_proxy: pd.DataFrame,
    authors_direct: pd.DataFrame,
    public_fwtw: pd.DataFrame,
) -> pd.DataFrame:
    """Align the paper benchmark and all three implementation routes by year."""

    inputs = (
        ("authors_kit_seven_round_proxy", seven_round_proxy),
        ("authors_kit_direct_full_leontief", authors_direct),
        ("public_fwtw_full_leontief", public_fwtw),
    )
    comparison = paper.copy()
    for prefix, frame in inputs:
        rename = {
            f"net_debt_{group}_relative_to_1982": (
                f"{prefix}_{group}_relative_to_1982"
            )
            for group in DISPLAY_GROUPS
        }
        comparison = comparison.merge(
            frame[["year", *rename]].rename(columns=rename),
            on="year",
            how="inner",
            validate="one_to_one",
        )
    for prefix, _ in inputs:
        for group in DISPLAY_GROUPS:
            comparison[f"{prefix}_error_{group}"] = (
                comparison[f"{prefix}_{group}_relative_to_1982"]
                - comparison[f"paper_{group}_relative_to_1982"]
            )
    return comparison.sort_values("year").reset_index(drop=True)


def calculate_comparison_metrics(comparison: pd.DataFrame) -> pd.DataFrame:
    """Calculate paper-benchmark fit metrics for every route and group."""

    rows: list[dict[str, float | str]] = []
    for prefix, label in APPROACH_LABELS.items():
        for group in DISPLAY_GROUPS:
            paper_column = f"paper_{group}_relative_to_1982"
            estimate_column = f"{prefix}_{group}_relative_to_1982"
            error = comparison[estimate_column] - comparison[paper_column]
            rows.append(
                {
                    "approach": label,
                    "approach_id": prefix,
                    "group": group,
                    "correlation": comparison[[paper_column, estimate_column]]
                    .corr()
                    .iloc[0, 1],
                    "mean_absolute_error_percentage_points": 100
                    * error.abs().mean(),
                    "root_mean_squared_error_percentage_points": 100
                    * error.pow(2).mean() ** 0.5,
                }
            )
    return pd.DataFrame(rows)


def calculate_same_vintage_operator_metrics(
    comparison: pd.DataFrame,
) -> pd.DataFrame:
    """Quantify full-Leontief minus seven-round changes on 2021 inputs."""

    headline_years = {2007, 2016}
    missing_years = headline_years.difference(comparison["year"])
    if missing_years:
        missing = ", ".join(str(year) for year in sorted(missing_years))
        raise ValueError(
            "Same-vintage operator metrics require headline years: "
            f"missing {missing}"
        )

    rows: list[dict[str, float | str]] = []
    for group in DISPLAY_GROUPS:
        direct = comparison[
            f"authors_kit_direct_full_leontief_{group}_relative_to_1982"
        ]
        proxy = comparison[
            f"authors_kit_seven_round_proxy_{group}_relative_to_1982"
        ]
        difference = direct - proxy
        difference_by_year = pd.Series(
            difference.to_numpy(), index=comparison["year"].to_numpy()
        )
        rows.append(
            {
                "group": group,
                "correlation": direct.corr(proxy),
                "mean_absolute_difference_percentage_points": 100
                * difference.abs().mean(),
                "maximum_absolute_difference_percentage_points": 100
                * difference.abs().max(),
                "difference_2007_percentage_points": 100
                * difference_by_year.loc[2007],
                "difference_2016_percentage_points": 100
                * difference_by_year.loc[2016],
            }
        )
    return pd.DataFrame(rows)


__all__ = [
    "APPROACH_LABELS",
    "build_method_comparison",
    "calculate_comparison_metrics",
    "calculate_same_vintage_operator_metrics",
]
