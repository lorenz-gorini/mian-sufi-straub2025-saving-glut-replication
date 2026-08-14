"""Debt-category saving contributions for the proposed research extension.

The Figure 8 network identifies stocks of home-mortgage and consumer-credit
claims.  This module constructs the matching borrower-side active-saving
contributions from the Figure 5 balance sheets.  It keeps liabilities in their
original negative balance-sheet sign when applying the paper's valuation
identity, so additional borrowing appears as a negative saving contribution.
"""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np
import pandas as pd

from .figure5_authors import GROUPS, known_asset_inflation


DEBT_SAVING_ASSETS: Mapping[str, str] = {
    "home_mortgage": "lhommort",
    "consumer_credit": "lcnscred",
}
DISPLAY_GROUPS = (*GROUPS, "bottom_99")


def construct_debt_saving_components(
    group_wealth: pd.DataFrame,
    valuation_inputs: pd.DataFrame,
) -> pd.DataFrame:
    """Construct write-down-adjusted saving contributions by debt category.

    For balance-sheet liability ``W[g,k,t] < 0`` and the paper's category-
    specific valuation factor ``pi[g,k,t]``, the active-saving contribution is

    ``S[g,k,t] = W[g,k,t] - (1 + pi[g,k,t]) * W[g,k,t-1]``.

    Parameters
    ----------
    group_wealth
        Annual four-group balance-sheet levels from
        :func:`unveiling.figure5_authors.construct_group_wealth`. Monetary
        values and ``NatInc`` are millions of current dollars.
    valuation_inputs
        Annual mortgage- and consumer-debt write-down factors from the authors'
        ``Ywealthreturns.dta`` file.

    Returns
    -------
    pandas.DataFrame
        One row per year, category, and group for 1963--2016. Liabilities owed
        and active borrowing are positive; active-saving contributions retain
        the paper's signed convention. The primary key is
        ``(year, category, group)``.
    """

    required_wealth = {"year", "NatInc"}
    required_wealth.update(
        f"h{asset}_{group}"
        for asset in DEBT_SAVING_ASSETS.values()
        for group in GROUPS
    )
    missing_wealth = sorted(required_wealth - set(group_wealth.columns))
    if missing_wealth:
        raise ValueError(
            f"debt saving components: missing wealth columns {missing_wealth}"
        )
    required_valuations = {
        "year",
        "ZIP_cdebt_wd10",
        "ZIP_cdebt_wd90",
        "ZIP_mdebt_wd10",
        "ZIP_mdebt_wd90",
    }
    missing_valuations = sorted(
        required_valuations - set(valuation_inputs.columns)
    )
    if missing_valuations:
        raise ValueError(
            "debt saving components: missing valuation columns "
            f"{missing_valuations}"
        )

    frame = group_wealth.merge(
        valuation_inputs[list(required_valuations)],
        on="year",
        how="left",
        validate="one_to_one",
        indicator=True,
    ).sort_values("year").reset_index(drop=True)
    if not frame["_merge"].eq("both").all():
        missing_years = frame.loc[frame["_merge"] != "both", "year"].tolist()
        raise ValueError(
            "debt saving components: unmatched valuation years "
            f"{missing_years}"
        )
    frame = frame.drop(columns="_merge")
    if not (frame["year"].diff().dropna() == 1).all():
        raise ValueError("debt saving components: years must be contiguous")

    records: list[dict[str, float | int | str]] = []
    for category, asset in DEBT_SAVING_ASSETS.items():
        group_values: dict[str, pd.DataFrame] = {}
        for group in GROUPS:
            signed_level = frame[f"h{asset}_{group}"]
            if (signed_level > 1e-6).any():
                raise ValueError(
                    f"debt saving components: {asset}/{group} must be nonpositive"
                )
            inflation = known_asset_inflation(
                frame,
                asset=asset,
                use_top_ten_write_down=group in {"top_1", "next_9"},
            )
            saving = signed_level - (1.0 + inflation) * signed_level.shift(1)
            group_values[group] = pd.DataFrame(
                {
                    "year": frame["year"],
                    "liability_stock_millions": -signed_level,
                    "active_saving_contribution_millions": saving,
                    "active_borrowing_millions": -saving,
                    "national_income_millions": frame["NatInc"],
                }
            )

        bottom_99 = pd.DataFrame({"year": frame["year"]})
        for column in (
            "liability_stock_millions",
            "active_saving_contribution_millions",
            "active_borrowing_millions",
        ):
            bottom_99[column] = sum(
                group_values[group][column]
                for group in ("next_9", "next_40", "bottom_50")
            )
        bottom_99["national_income_millions"] = frame["NatInc"]
        group_values["bottom_99"] = bottom_99

        for group, values in group_values.items():
            valid = values.loc[values["year"].between(1963, 2016)].copy()
            valid["category"] = category
            valid["group"] = group
            valid["liability_stock_to_national_income"] = (
                valid["liability_stock_millions"]
                / valid["national_income_millions"]
            )
            valid["active_saving_contribution_to_national_income"] = (
                valid["active_saving_contribution_millions"]
                / valid["national_income_millions"]
            )
            valid["active_borrowing_to_national_income"] = (
                valid["active_borrowing_millions"]
                / valid["national_income_millions"]
            )
            records.extend(valid.to_dict(orient="records"))

    output = pd.DataFrame(records)[
        [
            "year",
            "category",
            "group",
            "liability_stock_millions",
            "active_saving_contribution_millions",
            "active_borrowing_millions",
            "national_income_millions",
            "liability_stock_to_national_income",
            "active_saving_contribution_to_national_income",
            "active_borrowing_to_national_income",
        ]
    ].sort_values(["year", "category", "group"]).reset_index(drop=True)
    if output.duplicated(["year", "category", "group"]).any():
        raise ValueError("debt saving components: duplicate panel keys")
    expected_rows = 54 * len(DEBT_SAVING_ASSETS) * len(DISPLAY_GROUPS)
    if len(output) != expected_rows:
        raise ValueError(
            "debt saving components: incomplete 1963--2016 category panel"
        )
    numeric = output.select_dtypes(include=np.number)
    if not np.isfinite(numeric.to_numpy()).all():
        raise ValueError("debt saving components: non-finite output")
    return output


def summarize_debt_saving_periods(
    debt_saving_components: pd.DataFrame,
    *,
    periods: tuple[tuple[str, int, int], ...] = (
        ("1963–1982", 1963, 1982),
        ("1983–1997", 1983, 1997),
        ("1998–2007", 1998, 2007),
        ("2008–2016", 2008, 2016),
    ),
) -> pd.DataFrame:
    """Average category-specific borrowing and saving contributions by period.

    Returns a tidy extension of the paper's Table A2 debt contribution. Values
    in the ``*_pp_national_income`` columns are percentage points of national
    income per year, averaged over the inclusive period.
    """

    required = {
        "year",
        "category",
        "group",
        "active_saving_contribution_to_national_income",
        "active_borrowing_to_national_income",
    }
    missing = sorted(required - set(debt_saving_components.columns))
    if missing:
        raise ValueError(f"debt period summary: missing columns {missing}")
    records: list[dict[str, float | int | str]] = []
    for label, first_year, last_year in periods:
        period = debt_saving_components.loc[
            debt_saving_components["year"].between(first_year, last_year)
        ]
        expected_years = last_year - first_year + 1
        counts = period.groupby(["category", "group"])["year"].nunique()
        if counts.empty or not counts.eq(expected_years).all():
            raise ValueError(f"debt period summary: incomplete period {label}")
        grouped = period.groupby(["category", "group"], as_index=False).agg(
            mean_active_saving=(
                "active_saving_contribution_to_national_income",
                "mean",
            ),
            mean_active_borrowing=("active_borrowing_to_national_income", "mean"),
        )
        for row in grouped.itertuples(index=False):
            records.append(
                {
                    "period": label,
                    "first_year": first_year,
                    "last_year": last_year,
                    "category": row.category,
                    "group": row.group,
                    "mean_active_saving_contribution_pp_national_income": (
                        100.0 * row.mean_active_saving
                    ),
                    "mean_active_borrowing_pp_national_income": (
                        100.0 * row.mean_active_borrowing
                    ),
                }
            )
    return pd.DataFrame(records).sort_values(
        ["first_year", "category", "group"]
    ).reset_index(drop=True)


__all__ = [
    "DEBT_SAVING_ASSETS",
    "DISPLAY_GROUPS",
    "construct_debt_saving_components",
    "summarize_debt_saving_periods",
]
