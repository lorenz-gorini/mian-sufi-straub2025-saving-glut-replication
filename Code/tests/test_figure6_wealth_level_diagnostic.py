"""Tests for the exploratory Figure 6 wealth-level diagnostic."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from unveiling.figure5_authors import (
    ASSETS,
    construct_annual_saving,
    construct_group_wealth,
    load_aggregate_wealth,
    load_fine_wealth_shares,
    load_private_saving,
    load_valuation_inputs,
)
from unveiling.figure6_wealth_level_diagnostic import (
    construct_fine_wealth_profiles,
    load_demographics,
    summarize_wealth_windows,
)
from unveiling.wealth_groups import (
    FINE_COHORT_POPULATION_SHARES,
    FINE_COHORTS,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUTHOR_DATA = PROJECT_ROOT / "MSS2021Febreplicationkit" / "data"


def test_fine_profiles_preserve_wealth_income_and_saving_totals() -> None:
    aggregate = load_aggregate_wealth(
        AUTHOR_DATA / "finalfiles/YwealthFOF.dta"
    )
    shares = load_fine_wealth_shares(
        AUTHOR_DATA / "PSZusdina/Yszshares_fine.dta"
    )
    valuations = load_valuation_inputs(
        AUTHOR_DATA / "finalfiles/Ywealthreturns.dta"
    )
    annual_saving = construct_annual_saving(
        construct_group_wealth(aggregate, shares),
        valuations,
        load_private_saving(
            AUTHOR_DATA / "finalfiles/YinequalityNIPAanalysis.dta"
        ),
    )
    profiles = construct_fine_wealth_profiles(
        aggregate,
        shares,
        valuations,
        annual_saving,
        load_demographics(AUTHOR_DATA / "PSZusdina/parameters_mss.csv"),
    )

    assert len(profiles) == 54 * len(FINE_COHORTS)
    assert profiles["year"].min() == 1963
    assert profiles["year"].max() == 2016
    assert profiles.groupby("year").size().eq(len(FINE_COHORTS)).all()
    assert sum(FINE_COHORT_POPULATION_SHARES.values()) == pytest.approx(1.0)

    saving_total = profiles.groupby("year")["active_saving_millions"].sum()
    saving_expected = annual_saving.set_index("year")[
        "private_saving_millions"
    ]
    saving_error = (saving_total - saving_expected).abs() / annual_saving.set_index(
        "year"
    )["NatInc"]
    assert saving_error.max() < 1e-10

    income_total = profiles.groupby("year")["pretax_income_millions"].sum()
    aggregate_by_year = aggregate.set_index("year")
    assert np.allclose(
        income_total,
        aggregate_by_year.loc[income_total.index, "NatInc"],
        rtol=2e-6,
    )
    wealth_total = profiles.groupby("year")["wealth_millions"].sum()
    aggregate_net_wealth = sum(
        aggregate_by_year[f"h{asset}all"] for asset in ASSETS
    )
    assert np.allclose(
        wealth_total,
        aggregate_net_wealth.loc[wealth_total.index],
        rtol=2e-6,
        atol=1e-3,
    )

    windows = summarize_wealth_windows(profiles)
    assert len(windows) == 4 * len(FINE_COHORTS)
    selected = profiles.loc[
        profiles["year"].between(2007, 2016)
        & profiles["cohort"].eq("f80")
    ]
    expected_rate = (
        selected["active_saving_millions"].sum()
        / selected["pretax_income_millions"].sum()
    )
    observed_rate = windows.loc[
        windows["window"].eq("late_decade")
        & windows["cohort"].eq("f80"),
        "active_saving_to_pretax_income",
    ].item()
    assert observed_rate == pytest.approx(expected_rate)
