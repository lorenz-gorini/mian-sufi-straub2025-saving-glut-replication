"""Tests for the Figure 1 reconstruction from the authors' data."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from unveiling.figure1_authors import COMPONENT_COLUMNS, construct_authors_figure1


def _inputs() -> tuple[pd.DataFrame, ...]:
    balance_sheet = pd.DataFrame(
        {
            "year": [2000],
            "fl154090005q": [1_000.0],
            "fl153020005q": [10.0],
            "fl153030005q": [20.0],
            "fl153034005q": [30.0],
            "lm153061705q": [40.0],
            "lm153064205q": [50.0],
            "fl153040005q": [60.0],
            "fl153050005q": [80.0],
            "fl594090055q": [10.0],
            "lm153091003q": [5.0],
            "fl153090005q": [15.0],
        }
    )
    allocations = pd.DataFrame(
        {
            "year": [2000],
            "a_hh_absbnd": [1.0],
            "a_hh_fincbnd": [2.0],
            "a_hh_mreitbnd": [3.0],
            "a_hh_pdibnd": [4.0],
            "a_hh_equity": [200.0],
            "a_tot_equity": [500.0],
            "a_hh_nfcbnd": [20.0],
            "a_hh_nfcequity": [100.0],
            "a_hh_nfcothl": [5.0],
        }
    )
    crsp_equity = pd.DataFrame(
        {"year": [2000], "listed_financial_equity_millions": [100.0]}
    )
    national_income = pd.DataFrame(
        {"year": [2000], "national_income_millions": [500.0]}
    )
    return balance_sheet, allocations, crsp_equity, national_income


def test_component_sum_and_units_are_explicit() -> None:
    result = construct_authors_figure1(*_inputs())
    row = result.iloc[0]

    expected_components = 10 + 20 + 30 + 40 + 50 + 60 + 70 + 10 + 40
    assert row[list(COMPONENT_COLUMNS)].sum() == expected_components
    assert row["indirect_household_assets_millions"] == expected_components
    assert row["indirect_assets_to_national_income"] == pytest.approx(
        expected_components / 500
    )


def test_proxy_denominator_applies_documented_exclusions_once() -> None:
    result = construct_authors_figure1(*_inputs())
    row = result.iloc[0]

    expected_denominator = 1_000 - 10 - 5 - 15 - 20 - 100 - 5
    assert row["paper_scope_financial_assets_proxy_millions"] == (
        expected_denominator
    )
    assert row["indirect_share_proxy"] == pytest.approx(
        row["indirect_household_assets_millions"] / expected_denominator
    )


def test_merge_fails_when_an_annual_input_is_missing() -> None:
    balance_sheet, allocations, crsp_equity, national_income = _inputs()
    with pytest.raises(ValueError, match="annual merges lost observations"):
        construct_authors_figure1(
            balance_sheet,
            allocations.iloc[0:0],
            crsp_equity,
            national_income,
        )


def test_nonfinite_equity_share_fails_loudly() -> None:
    balance_sheet, allocations, crsp_equity, national_income = _inputs()
    allocations.loc[0, "a_tot_equity"] = np.nan
    with pytest.raises(ValueError, match="invalid household equity share"):
        construct_authors_figure1(
            balance_sheet, allocations, crsp_equity, national_income
        )
