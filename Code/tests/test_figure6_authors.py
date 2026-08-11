"""Tests for the exact-method old-input Figure 6 reconstruction."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from unveiling.figure5_authors import ASSETS
from unveiling.figure6_authors import (
    SHARE_CLASSES,
    build_rolling_profiles,
    collapse_percentile_share_chunk,
    construct_annual_percentile_profiles,
)


def test_raw_chunk_uses_bottom_40_and_one_percent_bins() -> None:
    chunk = pd.DataFrame(
        {
            "year": [1982, 1982, 1982],
            "wealth_ptile": [10, 40, 41],
            "dweght": [100_000.0, 200_000.0, 100_000.0],
            "hwequ": [1.0, 2.0, 8.0],
            "hwfix": [0.0, 0.0, 0.0],
            "hwbus": [0.0, 0.0, 0.0],
            "hwpen": [0.0, 0.0, 0.0],
            "ownerhome": [1.0, 1.0, 1.0],
            "ownermort": [-1.0, -1.0, -1.0],
            "nonmort": [-1.0, -1.0, -1.0],
            "taxbond": [1.0, 1.0, 1.0],
            "currency": [1.0, 1.0, 1.0],
            "muni": [1.0, 1.0, 1.0],
            "poinc": [10.0, 20.0, 40.0],
            "colexp": [1.0, 2.0, 4.0],
            "govin": [1.0, 2.0, 4.0],
            "prisupgov": [1.0, 2.0, 4.0],
        }
    )

    collapsed = collapse_percentile_share_chunk(chunk)

    assert collapsed.index.tolist() == [(1982, 40), (1982, 41)]
    assert collapsed.loc[(1982, 40), "population_weight"] == pytest.approx(3.0)
    assert collapsed.loc[(1982, 40), "hwequ"] == pytest.approx(5.0)
    assert collapsed.loc[(1982, 41), "ponog"] == pytest.approx(28.0)


def test_annual_profiles_close_equation_9c() -> None:
    years = [1962, 1963]
    aggregate = pd.DataFrame({"year": years, "NatInc": [1_000.0, 1_000.0]})
    for asset in ASSETS:
        aggregate[f"h{asset}all"] = 0.0
    aggregate["haforedepall"] = [100.0, 120.0]
    aggregate["hacorpequall"] = [100.0, 100.0]

    shares = []
    for year in years:
        for percentile_bin, share in ((40, 0.4), (100, 0.6)):
            record: dict[str, float | int | str | bool] = {
                "year": year,
                "percentile_bin": percentile_bin,
                "bin_label": "Bottom 40%" if percentile_bin == 40 else "Top 1%",
                "population_share": share,
                "uses_top_ten_debt_return": percentile_bin == 100,
            }
            record.update({f"share_{name}": share for name in SHARE_CLASSES})
            shares.append(record)
    percentile_shares = pd.DataFrame(shares)
    valuations = pd.DataFrame(
        {
            "year": years,
            "JST_housing_capgain": [0.0, 0.0],
            "ZIP_cdebt_wd10": [0.0, 0.0],
            "ZIP_cdebt_wd90": [0.0, 0.0],
            "ZIP_mdebt_wd10": [0.0, 0.0],
            "ZIP_mdebt_wd90": [0.0, 0.0],
        }
    )
    annual_saving = pd.DataFrame(
        {
            "year": [1963],
            "private_saving_millions": [20.0],
            "residual_equity_inflation": [0.0],
        }
    )
    disposable = pd.DataFrame(
        {
            "year": years,
            "personal_disposable_income_millions": [100.0, 100.0],
            "corporate_disposable_income_millions": [20.0, 20.0],
        }
    )
    demographics = pd.DataFrame(
        {
            "year": years,
            "totadults20": [10.0, 10.0],
            "nideflator": [1.0, 1.0],
        }
    )

    output = construct_annual_percentile_profiles(
        aggregate,
        percentile_shares,
        valuations,
        annual_saving,
        disposable,
        demographics,
    )

    assert len(output) == 2
    assert output["active_saving_millions"].sum() == pytest.approx(20.0)
    assert output["total_disposable_income_millions"].sum() == pytest.approx(
        120.0
    )
    weighted_rate = (
        output["net_saving_rate"]
        * output["total_disposable_income_millions"]
    ).sum()
    assert weighted_rate == pytest.approx(20.0)
    assert np.isfinite(output["real_mean_wealth_per_adult_2018_usd"]).all()


def test_rolling_profiles_average_consecutive_annual_rates() -> None:
    annual = pd.DataFrame(
        {
            "year": [2000, 2001, 2002, 2003, 2004, 2005],
            "percentile_bin": [80] * 6,
            "bin_label": ["79–80%"] * 6,
            "net_saving_rate": [0.10, 0.20, 0.30, 0.40, 0.50, 0.60],
        }
    )

    output = build_rolling_profiles(annual, window_years=5)

    assert output["window_end_year"].tolist() == [2004, 2005]
    assert output["window_start_year"].tolist() == [2000, 2001]
    assert output["rolling_mean_net_saving_rate"].tolist() == pytest.approx(
        [0.30, 0.40]
    )
