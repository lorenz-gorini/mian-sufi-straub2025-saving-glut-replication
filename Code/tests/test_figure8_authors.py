"""Tests for the best-feasible Figure 8 authors-kit proxy."""

from __future__ import annotations

from pathlib import Path

import pytest

from unveiling.figure8_authors import (
    construct_figure8_proxy,
    load_fine_debt_positions,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUTHOR_DATA = PROJECT_ROOT / "MSS2021Febreplicationkit" / "data"


def test_fine_positions_aggregate_and_net_debt_has_paper_sign() -> None:
    fine = load_fine_debt_positions(
        AUTHOR_DATA / "finalfiles/YinequalityFAanalysis.dta"
    )
    proxy, validation = construct_figure8_proxy(fine)

    assert proxy["year"].tolist() == list(range(1963, 2017))
    assert validation["relative_error"].abs().max() < 2e-6
    base = proxy.loc[proxy["year"] == 1982].iloc[0]
    for group in ("top_1", "next_9", "next_40", "bottom_50", "bottom_99"):
        assert base[f"net_debt_{group}_relative_to_1982"] == pytest.approx(0.0)

    year_2007 = proxy.loc[proxy["year"] == 2007].iloc[0]
    assert year_2007["net_debt_top_1_relative_to_1982"] > 0
    assert year_2007["net_debt_bottom_99_relative_to_1982"] < 0
    assert year_2007["net_debt_bottom_99_millions"] == pytest.approx(
        year_2007["net_debt_next_9_millions"]
        + year_2007["net_debt_next_40_millions"]
        + year_2007["net_debt_bottom_50_millions"]
    )
