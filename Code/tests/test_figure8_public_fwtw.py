"""Tests for the public-FWTW full-Leontief Figure 8 reconstruction."""

from __future__ import annotations

from pathlib import Path

import pytest

from unveiling.figure1 import read_fwtw
from unveiling.figure8_public_fwtw import (
    DINA_CLASSES,
    GROUPS,
    construct_public_fwtw_figure8,
    load_authors_national_income,
    load_distributional_shares,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUTHOR_DATA = PROJECT_ROOT / "MSS2021Febreplicationkit/data"


@pytest.fixture(scope="module")
def public_figure8_inputs():
    """Load the three immutable sources once for the module."""

    fwtw = read_fwtw(
        PROJECT_ROOT / "Data/raw/fwtw/fwtw_data_2026-06-18.csv"
    )
    shares = load_distributional_shares(
        AUTHOR_DATA / "PSZusdina/Yszshares_fine.dta"
    )
    income = load_authors_national_income(
        AUTHOR_DATA / "finalfiles/YwealthFOF.dta"
    )
    return fwtw, shares, income


def test_grouped_dina_shares_partition_each_asset_class(
    public_figure8_inputs,
) -> None:
    _, shares, _ = public_figure8_inputs
    assert shares["year"].tolist() == list(range(1963, 2017))
    for class_name in DINA_CLASSES:
        total = sum(shares[f"{class_name}_{group}"] for group in GROUPS)
        assert (total - 1.0).abs().max() < 1e-12


def test_full_leontief_network_and_net_debt_invariants(
    public_figure8_inputs,
) -> None:
    fwtw, shares, income = public_figure8_inputs
    result, sensitivity, diagnostics = construct_public_fwtw_figure8(
        fwtw,
        shares,
        income,
    )

    assert result["year"].tolist() == list(range(1963, 2017))
    assert sensitivity["year"].tolist() == list(range(1963, 2017))
    assert set(diagnostics["mode"]) == {"reoriented", "clipped"}
    assert diagnostics["published_instruments"].eq(31).all()
    assert diagnostics["substantive_sectors"].eq(25).all()
    assert diagnostics["spectral_radius"].lt(1.0).all()
    assert diagnostics["direct_row_sum_max_error"].lt(1e-12).all()
    assert diagnostics["omega_row_sum_max_error"].lt(1e-9).all()
    assert diagnostics["primary_asset_sum_error"].lt(1e-9).all()
    assert diagnostics["liability_sum_error_millions"].lt(1e-4).all()

    base = result.loc[result["year"] == 1982].iloc[0]
    for group in (*GROUPS, "bottom_99"):
        assert base[f"net_debt_{group}_relative_to_1982"] == pytest.approx(0.0)
    for measure in ("debt_assets", "debt_liabilities", "net_debt"):
        reconstructed = sum(
            result[f"{measure}_{group}_millions"]
            for group in ("next_9", "next_40", "bottom_50")
        )
        assert (
            result[f"{measure}_bottom_99_millions"] - reconstructed
        ).abs().max() < 1e-8


def test_reoriented_and_clipped_results_are_economically_close(
    public_figure8_inputs,
) -> None:
    fwtw, shares, income = public_figure8_inputs
    result, sensitivity, diagnostics = construct_public_fwtw_figure8(
        fwtw,
        shares,
        income,
    )
    for group in ("top_1", "bottom_99"):
        difference = (
            result[f"net_debt_{group}_relative_to_1982"]
            - sensitivity[f"net_debt_{group}_relative_to_1982"]
        ).abs()
        assert difference.max() < 0.02

    primary = diagnostics.loc[diagnostics["mode"] == "reoriented"]
    assert primary["negative_input_cells"].gt(0).any()
    assert primary["omega_minimum_share"].min() >= -1e-12
    assert primary["primary_minimum_share"].min() >= -1e-12
