"""Tests for Figure 5 reconstructed from authors-kit inputs."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from unveiling.figure5_authors import (
    GROUPS,
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


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUTHOR_DATA = PROJECT_ROOT / "MSS2021Febreplicationkit" / "data"


def test_display_uses_trailing_window_and_subtracts_1982() -> None:
    years = np.arange(1963, 1984)
    annual = pd.DataFrame({"year": years})
    for offset, group in enumerate((*GROUPS, "bottom_99")):
        annual[f"saving_{group}_to_national_income"] = (
            0.01 * offset + 0.001 * (years - 1963)
        )

    display = apply_figure5_display(annual)

    assert display["year"].iloc[0] == 1972
    for group in (*GROUPS, "bottom_99"):
        base = display.loc[
            display["year"] == 1982,
            f"{group}_relative_to_1982",
        ].iloc[0]
        assert base == pytest.approx(0.0)
    top_1_1983 = display.loc[
        display["year"] == 1983,
        "top_1_relative_to_1982",
    ].iloc[0]
    assert top_1_1983 == pytest.approx(0.001)


def test_author_inputs_close_to_nipa_and_old_coarse_benchmark() -> None:
    """The residual return closes saving and fine groups stay near old cells."""

    wealth = construct_group_wealth(
        load_aggregate_wealth(AUTHOR_DATA / "finalfiles/YwealthFOF.dta"),
        load_fine_wealth_shares(
            AUTHOR_DATA / "PSZusdina/Yszshares_fine.dta"
        ),
    )
    annual = construct_annual_saving(
        wealth,
        load_valuation_inputs(
            AUTHOR_DATA / "finalfiles/Ywealthreturns.dta"
        ),
        load_private_saving(
            AUTHOR_DATA / "finalfiles/YinequalityNIPAanalysis.dta"
        ),
    )
    validation = build_saving_validation(
        annual,
        load_saving_benchmark(
            AUTHOR_DATA / "finalfiles/Ysavingwealth.dta"
        ),
    )

    closure = (
        annual["reconstructed_private_saving_millions"]
        - annual["private_saving_millions"]
    ) / annual["NatInc"]
    assert closure.abs().max() < 1e-10
    assert validation["error"].abs().max() < 0.003
    assert annual["year"].tolist() == list(range(1963, 2017))
