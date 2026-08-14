"""Tests for the 2021-direct-cell full-Leontief Figure 8 route."""

from __future__ import annotations

from pathlib import Path
import re

import numpy as np
import pandas as pd
import pytest

from unveiling.figure8_2021_direct import (
    DEBT_CATEGORIES,
    DIRECT_SOURCE_COLUMNS,
    GROUPS,
    INTERMEDIARIES,
    build_debt_composition_panel,
    construct_2021_direct_full_leontief,
    load_2021_direct_cells,
    load_authors_national_income,
    load_distributional_shares,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUTHOR_DATA = PROJECT_ROOT / "MSS2021Febreplicationkit/data"


@pytest.fixture(scope="module")
def direct_figure8_outputs():
    """Build the immutable-source route once for the module."""

    direct = load_2021_direct_cells(
        AUTHOR_DATA / "finalfiles/Yunveilhhd.dta"
    )
    shares = load_distributional_shares(
        AUTHOR_DATA / "PSZusdina/Yszshares_fine.dta"
    )
    income = load_authors_national_income(
        AUTHOR_DATA / "finalfiles/YwealthFOF.dta"
    )
    result, diagnostics, components = construct_2021_direct_full_leontief(
        direct,
        shares,
        income,
    )
    return direct, result, diagnostics, components


def test_source_contract_excludes_every_seven_round_output() -> None:
    prohibited = re.compile(
        r"(?:_hhd[1-7]$|^a_hh_hhd$|_hhdSZ$|^a_(?:gov|row|oth)_hhd$)"
    )
    assert len(DIRECT_SOURCE_COLUMNS) == len(set(DIRECT_SOURCE_COLUMNS))
    assert not [column for column in DIRECT_SOURCE_COLUMNS if prohibited.search(column)]


def test_direct_source_has_complete_sample_and_balanced_primary_debt(
    direct_figure8_outputs,
) -> None:
    direct, _, _, _ = direct_figure8_outputs
    assert direct["year"].tolist() == list(range(1963, 2017))
    debt = direct["d_hh_hmort"] + direct["d_hh_ccred"]
    relative_error = (direct["a_hhd_tot"] - debt).abs() / debt
    assert relative_error.max() < 1e-6


def test_full_leontief_and_figure8_accounting_invariants(
    direct_figure8_outputs,
) -> None:
    _, result, diagnostics, components = direct_figure8_outputs
    assert result["year"].tolist() == list(range(1963, 2017))
    assert diagnostics["round_variables_read"].eq(0).all()
    assert diagnostics["coarsened_intermediaries"].eq(len(INTERMEDIARIES)).all()
    assert diagnostics["active_intermediaries"].between(7, 8).all()
    assert diagnostics["spectral_radius"].lt(1.0).all()
    assert diagnostics["direct_row_sum_max_error"].lt(1e-12).all()
    assert diagnostics["omega_row_sum_max_error"].lt(1e-12).all()
    assert diagnostics["primary_asset_sum_error"].lt(1e-12).all()
    assert diagnostics["category_primary_asset_sum_max_error"].lt(1e-12).all()
    assert diagnostics["liability_sum_error_millions"].lt(1e-5).all()
    assert diagnostics["category_liability_sum_max_error_millions"].lt(1e-5).all()
    assert diagnostics["category_additivity_max_error_millions"].lt(1e-5).all()
    assert diagnostics["authors_source_debt_margin_error_millions"].le(2.0).all()
    assert diagnostics["unassigned_ultimate_debt_share"].between(0.0, 0.11).all()
    assert diagnostics["negative_direct_cells_clipped"].gt(0).all()

    margin_error = (
        components["allocated_millions"]
        - components["liability_margin_millions"]
    ).abs()
    assert margin_error.max() < 1e-5
    assert not components["fallback_to_unassigned"].any()

    base = result.loc[result["year"] == 1982].iloc[0]
    for group in (*GROUPS, "bottom_99"):
        assert base[f"net_debt_{group}_relative_to_1982"] == pytest.approx(0.0)
    for measure in ("debt_assets", "debt_liabilities", "net_debt"):
        lower_groups = sum(
            result[f"{measure}_{group}_millions"]
            for group in ("next_9", "next_40", "bottom_50")
        )
        assert np.allclose(
            result[f"{measure}_bottom_99_millions"],
            lower_groups,
            atol=1e-8,
            rtol=0.0,
        )
        for group in (*GROUPS, "bottom_99"):
            category_sum = sum(
                result[f"{measure}_{category}_{group}_millions"]
                for category in DEBT_CATEGORIES
            )
            assert np.allclose(
                result[f"{measure}_{group}_millions"],
                category_sum,
                atol=1e-8,
                rtol=0.0,
            )

    panel = build_debt_composition_panel(result)
    assert len(panel) == 54 * 2 * 5
    assert not panel.duplicated(["year", "category", "group"]).any()
    assert set(panel["category"]) == set(DEBT_CATEGORIES)
    assert (
        panel.loc[panel["year"] == 1982, "net_debt_relative_to_1982"].abs().max()
        < 1e-12
    )


def test_reconstructed_mutual_fund_weights_match_authors_saved_weights(
    direct_figure8_outputs,
) -> None:
    """Validate our raw-variable reconstruction against a non-unveiling field."""

    _, _, diagnostics, _ = direct_figure8_outputs
    saved = pd.read_stata(
        AUTHOR_DATA / "finalfiles/YinequalityFAanalysis.dta",
        columns=[
            "year",
            "a_mufu_equ_sh",
            "a_mufu_bnd_sh",
            "a_mufu_mun_sh",
        ],
        convert_categoricals=False,
    )
    saved = saved.loc[saved["year"].between(1963, 2016)]
    aligned = diagnostics.merge(saved, on="year", validate="one_to_one")
    for reconstructed, benchmark in (
        ("mutual_fund_equity_share", "a_mufu_equ_sh"),
        ("mutual_fund_taxbond_share", "a_mufu_bnd_sh"),
        ("mutual_fund_muni_share", "a_mufu_mun_sh"),
    ):
        assert np.allclose(
            aligned[reconstructed],
            aligned[benchmark],
            atol=2e-7,
            rtol=0.0,
        )
