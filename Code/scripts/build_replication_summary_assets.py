"""Build the generated numerical macros used by the short replication brief.

The script reads the aligned paper/reconstruction comparison tables produced
by the three existing figure pipelines. It never reads plotted pixels or
changes the empirical series; it only summarizes verified comparison outputs.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED = PROJECT_ROOT / "Data" / "processed"
OUTPUT = PROJECT_ROOT / "Report" / "generated" / "replication_summary_values.tex"


def validate_comparison(
    frame: pd.DataFrame,
    required_columns: tuple[str, ...],
    source_path: Path,
) -> None:
    """Validate an aligned annual comparison table at its reporting boundary.

    Parameters
    ----------
    frame
        Annual comparison data. Each row must identify one year.
    required_columns
        Numeric series needed for the reported metrics.
    source_path
        Input path included in raised errors for provenance.

    Raises
    ------
    ValueError
        If years are missing or duplicated, required columns are absent, or
        reported series contain missing values.
    """

    required = {"year", *required_columns}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"{source_path}: missing columns {sorted(missing)}")
    if frame["year"].isna().any() or frame["year"].duplicated().any():
        raise ValueError(f"{source_path}: year must be a nonmissing primary key")
    if frame[list(required_columns)].isna().any().any():
        raise ValueError(f"{source_path}: reported series contain missing values")


def correlation(frame: pd.DataFrame, paper: str, replication: str) -> float:
    """Return the Pearson correlation of two aligned annual series."""

    return float(frame[paper].corr(frame[replication]))


def mean_absolute_error_pp(frame: pd.DataFrame, error: str) -> float:
    """Return an aligned error column's mean absolute error in percentage points."""

    return float(100 * frame[error].abs().mean())


def main() -> None:
    """Write LaTeX macros for the short replication brief."""

    figure1_path = PROCESSED / "figure1_authors_comparison.csv"
    figure5_path = PROCESSED / "figure5_authors_comparison.csv"
    figure8_path = PROCESSED / "figure8_method_comparison.csv"
    figure8_operator_path = (
        PROCESSED / "figure8_2021_operator_comparison_metrics.csv"
    )
    figure1 = pd.read_csv(figure1_path)
    figure5 = pd.read_csv(figure5_path)
    figure8 = pd.read_csv(figure8_path)
    figure8_operator = pd.read_csv(figure8_operator_path)

    validate_comparison(
        figure1,
        (
            "paper_indirect_assets_to_national_income",
            "indirect_assets_to_national_income",
            "level_error",
        ),
        figure1_path,
    )
    validate_comparison(
        figure5,
        (
            "paper_top_1_relative_to_1982",
            "authors_top_1_relative_to_1982",
            "paper_bottom_99_relative_to_1982",
            "authors_bottom_99_relative_to_1982",
            "error_top_1",
            "error_bottom_99",
        ),
        figure5_path,
    )
    validate_comparison(
        figure8,
        (
            "paper_top_1_relative_to_1982",
            "authors_kit_direct_full_leontief_top_1_relative_to_1982",
            "paper_bottom_99_relative_to_1982",
            "authors_kit_direct_full_leontief_bottom_99_relative_to_1982",
            "authors_kit_direct_full_leontief_error_top_1",
            "authors_kit_direct_full_leontief_error_bottom_99",
            "public_fwtw_full_leontief_error_top_1",
            "public_fwtw_full_leontief_error_bottom_99",
        ),
        figure8_path,
    )
    required_operator_columns = {
        "group",
        "mean_absolute_difference_percentage_points",
    }
    missing_operator_columns = required_operator_columns.difference(
        figure8_operator.columns
    )
    if missing_operator_columns:
        raise ValueError(
            f"{figure8_operator_path}: missing columns "
            f"{sorted(missing_operator_columns)}"
        )
    if figure8_operator["group"].duplicated().any():
        raise ValueError(f"{figure8_operator_path}: group must be unique")

    operator_by_group = figure8_operator.set_index("group")
    for group in ("top_1", "bottom_99"):
        if group not in operator_by_group.index:
            raise ValueError(f"{figure8_operator_path}: missing group {group}")

    figure8_2007 = figure8.loc[figure8["year"] == 2007]
    if len(figure8_2007) != 1:
        raise ValueError(f"{figure8_path}: expected exactly one observation for 2007")
    row_2007 = figure8_2007.iloc[0]

    macros = {
        "SummaryFigureOneStartYear": int(figure1["year"].min()),
        "SummaryFigureOneEndYear": int(figure1["year"].max()),
        "SummaryFigureOneCorrelation": (
            f"{correlation(figure1, 'paper_indirect_assets_to_national_income', 'indirect_assets_to_national_income'):.3f}"
        ),
        "SummaryFigureOneMAE": f"{mean_absolute_error_pp(figure1, 'level_error'):.1f}",
        "SummaryFigureFiveTopCorrelation": (
            f"{correlation(figure5, 'paper_top_1_relative_to_1982', 'authors_top_1_relative_to_1982'):.3f}"
        ),
        "SummaryFigureFiveBottomCorrelation": (
            f"{correlation(figure5, 'paper_bottom_99_relative_to_1982', 'authors_bottom_99_relative_to_1982'):.3f}"
        ),
        "SummaryFigureFiveTopMAE": f"{mean_absolute_error_pp(figure5, 'error_top_1'):.2f}",
        "SummaryFigureFiveBottomMAE": f"{mean_absolute_error_pp(figure5, 'error_bottom_99'):.2f}",
        "SummaryFigureEightPrimaryTopCorrelation": (
            f"{correlation(figure8, 'paper_top_1_relative_to_1982', 'authors_kit_direct_full_leontief_top_1_relative_to_1982'):.3f}"
        ),
        "SummaryFigureEightPrimaryBottomCorrelation": (
            f"{correlation(figure8, 'paper_bottom_99_relative_to_1982', 'authors_kit_direct_full_leontief_bottom_99_relative_to_1982'):.3f}"
        ),
        "SummaryFigureEightPrimaryTopMAE": (
            f"{mean_absolute_error_pp(figure8, 'authors_kit_direct_full_leontief_error_top_1'):.2f}"
        ),
        "SummaryFigureEightPrimaryBottomMAE": (
            f"{mean_absolute_error_pp(figure8, 'authors_kit_direct_full_leontief_error_bottom_99'):.2f}"
        ),
        "SummaryFigureEightPublicTopMAE": (
            f"{mean_absolute_error_pp(figure8, 'public_fwtw_full_leontief_error_top_1'):.2f}"
        ),
        "SummaryFigureEightPublicBottomMAE": (
            f"{mean_absolute_error_pp(figure8, 'public_fwtw_full_leontief_error_bottom_99'):.2f}"
        ),
        "SummaryFigureEightPrimaryBottomTwoThousandSeven": (
            f"{100 * row_2007['authors_kit_direct_full_leontief_bottom_99_relative_to_1982']:.2f}"
        ),
        "SummaryFigureEightPaperTopTwoThousandSeven": (
            f"{100 * row_2007['paper_top_1_relative_to_1982']:.2f}"
        ),
        "SummaryFigureEightPrimaryTopTwoThousandSeven": (
            f"{100 * row_2007['authors_kit_direct_full_leontief_top_1_relative_to_1982']:.2f}"
        ),
        "SummaryFigureEightPaperBottomTwoThousandSeven": (
            f"{100 * row_2007['paper_bottom_99_relative_to_1982']:.2f}"
        ),
        "SummaryFigureEightOperatorTopMeanAbsDiff": (
            f"{operator_by_group.loc['top_1', 'mean_absolute_difference_percentage_points']:.2f}"
        ),
        "SummaryFigureEightOperatorBottomMeanAbsDiff": (
            f"{operator_by_group.loc['bottom_99', 'mean_absolute_difference_percentage_points']:.2f}"
        ),
    }

    lines = [
        "% Generated by Code/scripts/build_replication_summary_assets.py.",
        "% Do not edit numerical values by hand.",
    ]
    lines.extend(f"\\newcommand{{\\{name}}}{{{value}}}" for name, value in macros.items())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
