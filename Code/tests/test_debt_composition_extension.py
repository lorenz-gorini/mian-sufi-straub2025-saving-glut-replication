"""Tests for the debt-composition research extension."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

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


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUTHOR_DATA = PROJECT_ROOT / "MSS2021Febreplicationkit" / "data"


@pytest.fixture(scope="module")
def debt_saving_panel():
    """Build the immutable-source saving contribution panel once."""

    wealth = construct_group_wealth(
        load_aggregate_wealth(AUTHOR_DATA / "finalfiles/YwealthFOF.dta"),
        load_fine_wealth_shares(
            AUTHOR_DATA / "PSZusdina/Yszshares_fine.dta"
        ),
    )
    return construct_debt_saving_components(
        wealth,
        load_valuation_inputs(
            AUTHOR_DATA / "finalfiles/Ywealthreturns.dta"
        ),
    )


def test_debt_saving_panel_has_expected_keys_and_signs(debt_saving_panel) -> None:
    assert len(debt_saving_panel) == 54 * 2 * 5
    assert not debt_saving_panel.duplicated(
        ["year", "category", "group"]
    ).any()
    assert debt_saving_panel["year"].min() == 1963
    assert debt_saving_panel["year"].max() == 2016
    assert debt_saving_panel["liability_stock_millions"].ge(0.0).all()
    assert np.allclose(
        debt_saving_panel["active_borrowing_millions"],
        -debt_saving_panel["active_saving_contribution_millions"],
        atol=1e-10,
        rtol=0.0,
    )

    for category in ("home_mortgage", "consumer_credit"):
        category_panel = debt_saving_panel.loc[
            debt_saving_panel["category"] == category
        ]
        for year in category_panel["year"].unique():
            current = category_panel.loc[category_panel["year"] == year]
            lower = current.set_index("group").loc[
                ["next_9", "next_40", "bottom_50"],
                "active_saving_contribution_millions",
            ].sum()
            bottom_99 = current.loc[
                current["group"] == "bottom_99",
                "active_saving_contribution_millions",
            ].iloc[0]
            assert bottom_99 == pytest.approx(lower)


def test_period_summary_is_complete_and_uses_percentage_points(
    debt_saving_panel,
) -> None:
    summary = summarize_debt_saving_periods(debt_saving_panel)
    assert len(summary) == 4 * 2 * 5
    assert not summary.duplicated(["period", "category", "group"]).any()
    assert np.allclose(
        summary["mean_active_borrowing_pp_national_income"],
        -summary["mean_active_saving_contribution_pp_national_income"],
        atol=1e-12,
        rtol=0.0,
    )
