"""Generate numerical LaTeX macros for the compact extension proposal.

The script reads the verified same-vintage debt-composition outputs. It does
not recompute the underlying stocks, saving contributions, or unveiled net
positions; it validates their reporting keys and exports only selected values
used by the course-facing proposal.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED = PROJECT_ROOT / "Data" / "processed"
OUTPUT = (
    PROJECT_ROOT
    / "Extension_Proposal"
    / "generated"
    / "extension_proposal_values.tex"
)


def validate_unique_panel(
    frame: pd.DataFrame,
    *,
    required_columns: set[str],
    key_columns: list[str],
    source_path: Path,
) -> None:
    """Validate one generated reporting table at its consumption boundary.

    Parameters
    ----------
    frame
        Generated reporting table.
    required_columns
        Columns needed by the proposal.
    key_columns
        Columns that must identify rows uniquely.
    source_path
        Input path used in error messages.

    Raises
    ------
    ValueError
        If required fields are absent, keys are missing or duplicated, or a
        reported numerical value is missing.
    """

    missing = required_columns.difference(frame.columns)
    if missing:
        raise ValueError(f"{source_path}: missing columns {sorted(missing)}")
    if frame[key_columns].isna().any().any() or frame.duplicated(key_columns).any():
        raise ValueError(f"{source_path}: {key_columns} must be a nonmissing key")


def select_metric(
    frame: pd.DataFrame,
    *,
    metric: str,
    category: str,
    group: str,
    source_path: Path,
) -> float:
    """Return one uniquely identified headline metric."""

    selected = frame.loc[
        frame["metric"].eq(metric)
        & frame["category"].eq(category)
        & frame["group"].eq(group),
        "value",
    ]
    if len(selected) != 1 or selected.isna().any():
        raise ValueError(
            f"{source_path}: expected one value for "
            f"({metric}, {category}, {group})"
        )
    return float(selected.iloc[0])


def select_period_metric(
    frame: pd.DataFrame,
    *,
    period: str,
    category: str,
    group: str,
    source_path: Path,
) -> float:
    """Return one period-average active-saving contribution."""

    selected = frame.loc[
        frame["period"].eq(period)
        & frame["category"].eq(category)
        & frame["group"].eq(group),
        "mean_active_saving_contribution_pp_national_income",
    ]
    if len(selected) != 1 or selected.isna().any():
        raise ValueError(
            f"{source_path}: expected one value for "
            f"({period}, {category}, {group})"
        )
    return float(selected.iloc[0])


def signed(value: float) -> str:
    """Format a percentage-point estimate with an explicit sign."""

    if abs(value) < 0.005:
        return "0.00"
    return f"{value:+.2f}"


def main() -> None:
    """Write the generated extension-proposal metric macros."""

    metrics_path = PROCESSED / "debt_composition_presentation_metrics.csv"
    periods_path = PROCESSED / "debt_composition_period_summary.csv"
    metrics = pd.read_csv(metrics_path)
    periods = pd.read_csv(periods_path)
    periods["period"] = periods["period"].str.replace("\N{EN DASH}", "--")

    validate_unique_panel(
        metrics,
        required_columns={"metric", "category", "group", "value"},
        key_columns=["metric", "category", "group"],
        source_path=metrics_path,
    )
    validate_unique_panel(
        periods,
        required_columns={
            "period",
            "category",
            "group",
            "mean_active_saving_contribution_pp_national_income",
        },
        key_columns=["period", "category", "group"],
        source_path=periods_path,
    )
    if metrics["value"].isna().any():
        raise ValueError(f"{metrics_path}: value must be nonmissing")
    if periods[
        "mean_active_saving_contribution_pp_national_income"
    ].isna().any():
        raise ValueError(
            f"{periods_path}: active-saving contribution must be nonmissing"
        )

    macro_specs = {
        "ExtensionLiabilityMortgageTopOne": (
            "liability_change_1982_to_2007_pp_ni",
            "home_mortgage",
            "top_1",
        ),
        "ExtensionLiabilityMortgageNextForty": (
            "liability_change_1982_to_2007_pp_ni",
            "home_mortgage",
            "next_40",
        ),
        "ExtensionLiabilityMortgageBottomFifty": (
            "liability_change_1982_to_2007_pp_ni",
            "home_mortgage",
            "bottom_50",
        ),
        "ExtensionLiabilityConsumerTopOne": (
            "liability_change_1982_to_2007_pp_ni",
            "consumer_credit",
            "top_1",
        ),
        "ExtensionLiabilityConsumerNextForty": (
            "liability_change_1982_to_2007_pp_ni",
            "consumer_credit",
            "next_40",
        ),
        "ExtensionLiabilityConsumerBottomFifty": (
            "liability_change_1982_to_2007_pp_ni",
            "consumer_credit",
            "bottom_50",
        ),
        "ExtensionSavingMortgageTopOne": (
            "mean_active_saving_contribution_1998_2007_pp_ni",
            "home_mortgage",
            "top_1",
        ),
        "ExtensionSavingMortgageNextForty": (
            "mean_active_saving_contribution_1998_2007_pp_ni",
            "home_mortgage",
            "next_40",
        ),
        "ExtensionSavingMortgageBottomFifty": (
            "mean_active_saving_contribution_1998_2007_pp_ni",
            "home_mortgage",
            "bottom_50",
        ),
        "ExtensionSavingConsumerTopOne": (
            "mean_active_saving_contribution_1998_2007_pp_ni",
            "consumer_credit",
            "top_1",
        ),
        "ExtensionSavingConsumerNextForty": (
            "mean_active_saving_contribution_1998_2007_pp_ni",
            "consumer_credit",
            "next_40",
        ),
        "ExtensionSavingConsumerBottomFifty": (
            "mean_active_saving_contribution_1998_2007_pp_ni",
            "consumer_credit",
            "bottom_50",
        ),
        "ExtensionNetMortgageTopOne": (
            "net_position_change_1982_to_2007_pp_ni",
            "home_mortgage",
            "top_1",
        ),
        "ExtensionNetMortgageNextForty": (
            "net_position_change_1982_to_2007_pp_ni",
            "home_mortgage",
            "next_40",
        ),
        "ExtensionNetMortgageBottomFifty": (
            "net_position_change_1982_to_2007_pp_ni",
            "home_mortgage",
            "bottom_50",
        ),
        "ExtensionNetConsumerTopOne": (
            "net_position_change_1982_to_2007_pp_ni",
            "consumer_credit",
            "top_1",
        ),
        "ExtensionNetConsumerNextForty": (
            "net_position_change_1982_to_2007_pp_ni",
            "consumer_credit",
            "next_40",
        ),
        "ExtensionNetConsumerBottomFifty": (
            "net_position_change_1982_to_2007_pp_ni",
            "consumer_credit",
            "bottom_50",
        ),
    }
    macros = {
        name: signed(
            select_metric(
                metrics,
                metric=metric,
                category=category,
                group=group,
                source_path=metrics_path,
            )
        )
        for name, (metric, category, group) in macro_specs.items()
    }

    for name, period, category in (
        ("ExtensionBottomNinetyNineMortgageBoom", "1998--2007", "home_mortgage"),
        ("ExtensionBottomNinetyNineMortgagePost", "2008--2016", "home_mortgage"),
        ("ExtensionBottomNinetyNineConsumerBoom", "1998--2007", "consumer_credit"),
        ("ExtensionBottomNinetyNineConsumerPost", "2008--2016", "consumer_credit"),
    ):
        macros[name] = signed(
            select_period_metric(
                periods,
                period=period,
                category=category,
                group="bottom_99",
                source_path=periods_path,
            )
        )

    lines = [
        "% Generated by Code/scripts/build_extension_proposal_assets.py.",
        "% Do not edit numerical values by hand.",
    ]
    lines.extend(f"\\newcommand{{\\{name}}}{{{value}}}" for name, value in macros.items())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
