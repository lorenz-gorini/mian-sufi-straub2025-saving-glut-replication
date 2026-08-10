"""Tests for the Figure 1 reconstruction from the authors' data."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from unveiling.figure1_authors import (
    BOND_BENCHMARK_COLUMNS,
    COMPONENT_COLUMNS,
    construct_author_bond_allocations,
    construct_authors_figure1,
    load_author_bond_benchmark,
    load_author_bond_inputs,
    load_author_equity_shares,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


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
    bonds = pd.DataFrame(
        {
            "year": [2000],
            "a_hh_absbnd": [1.0],
            "a_hh_fincbnd": [2.0],
            "a_hh_mreitbnd": [3.0],
            "a_hh_pdibnd": [4.0],
        }
    )
    equity_shares = pd.DataFrame(
        {
            "year": [2000],
            "a_hh_equity": [200.0],
            "a_tot_equity": [500.0],
        }
    )
    denominator_allocations = pd.DataFrame(
        {
            "year": [2000],
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
    return (
        balance_sheet,
        bonds,
        equity_shares,
        denominator_allocations,
        crsp_equity,
        national_income,
    )


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
    (
        balance_sheet,
        bonds,
        equity_shares,
        denominator_allocations,
        crsp_equity,
        national_income,
    ) = _inputs()
    with pytest.raises(ValueError, match="annual merges lost observations"):
        construct_authors_figure1(
            balance_sheet,
            bonds.iloc[0:0],
            equity_shares,
            denominator_allocations,
            crsp_equity,
            national_income,
        )


def test_nonfinite_equity_share_fails_loudly() -> None:
    (
        balance_sheet,
        bonds,
        equity_shares,
        denominator_allocations,
        crsp_equity,
        national_income,
    ) = _inputs()
    equity_shares.loc[0, "a_tot_equity"] = np.nan
    with pytest.raises(ValueError, match="invalid household equity share"):
        construct_authors_figure1(
            balance_sheet,
            bonds,
            equity_shares,
            denominator_allocations,
            crsp_equity,
            national_income,
        )


def test_raw_bond_reconstruction_matches_supplied_stata_cells() -> None:
    """The Python missing-cell allocation reproduces the supplied benchmark."""

    panel = (
        PROJECT_ROOT
        / "MSS2021Febreplicationkit"
        / "data"
        / "fof"
        / "LQpanel_2019Q1.dta"
    )
    benchmark_path = (
        PROJECT_ROOT
        / "Data"
        / "processed"
        / "finalfiles"
        / "Yunveilhhd.dta"
    )
    reconstructed = construct_author_bond_allocations(
        load_author_bond_inputs(panel)
    )
    benchmark = load_author_bond_benchmark(benchmark_path)
    merged = reconstructed.merge(
        benchmark,
        on="year",
        validate="one_to_one",
        suffixes=("_python", "_stata"),
    )
    for column in BOND_BENCHMARK_COLUMNS[1:]:
        error = (
            merged[f"{column}_python"] - merged[f"{column}_stata"]
        ).abs()
        assert error.max() < 0.05


def test_raw_equity_shares_match_supplied_stata_intermediates() -> None:
    """The raw equity aggregation reproduces the old prepared variables."""

    panel = (
        PROJECT_ROOT
        / "MSS2021Febreplicationkit"
        / "data"
        / "fof"
        / "LQpanel_2019Q1.dta"
    )
    benchmark_path = (
        PROJECT_ROOT
        / "Data"
        / "processed"
        / "finalfiles"
        / "Yunveilhhd.dta"
    )
    reconstructed = load_author_equity_shares(panel)
    benchmark = pd.read_stata(
        benchmark_path,
        columns=["year", "a_hh_equity", "a_tot_equity"],
        convert_categoricals=False,
    )
    benchmark = benchmark.loc[benchmark["year"].between(1963, 2016)].copy()
    merged = reconstructed.merge(
        benchmark,
        on="year",
        validate="one_to_one",
        suffixes=("_python", "_stata"),
    )
    for column in ("a_hh_equity", "a_tot_equity"):
        np.testing.assert_array_equal(
            merged[f"{column}_python"], merged[f"{column}_stata"]
        )
