"""Tests for the explicit three-route Figure 8 comparison layer."""

from __future__ import annotations

import numpy as np
import pandas as pd

from unveiling.figure8_comparison import (
    build_method_comparison,
    calculate_comparison_metrics,
    calculate_same_vintage_operator_metrics,
)
from unveiling.figure8_public_fwtw import DISPLAY_GROUPS


def _route(offset: float) -> pd.DataFrame:
    data: dict[str, list[float] | list[int]] = {
        "year": [1982, 1983, 2007, 2016]
    }
    for index, group in enumerate(DISPLAY_GROUPS, start=1):
        data[f"net_debt_{group}_relative_to_1982"] = [
            0.0,
            index * 0.01 + offset,
            index * 0.02 + offset,
            index * 0.03 + offset,
        ]
    return pd.DataFrame(data)


def test_comparison_keeps_all_three_route_names_and_metrics() -> None:
    paper = _route(0.0).rename(
        columns={
            f"net_debt_{group}_relative_to_1982": (
                f"paper_{group}_relative_to_1982"
            )
            for group in DISPLAY_GROUPS
        }
    )
    comparison = build_method_comparison(
        paper,
        _route(0.001),
        _route(0.002),
        _route(0.003),
    )
    expected_prefixes = (
        "authors_kit_seven_round_proxy",
        "authors_kit_direct_full_leontief",
        "public_fwtw_full_leontief",
    )
    for prefix in expected_prefixes:
        assert f"{prefix}_top_1_relative_to_1982" in comparison
        assert f"{prefix}_error_bottom_99" in comparison

    metrics = calculate_comparison_metrics(comparison)
    assert set(metrics["approach_id"]) == set(expected_prefixes)
    assert len(metrics) == 3 * len(DISPLAY_GROUPS)
    operator = calculate_same_vintage_operator_metrics(comparison)
    assert len(operator) == len(DISPLAY_GROUPS)
    assert np.allclose(
        operator["difference_2007_percentage_points"], 0.1
    )
