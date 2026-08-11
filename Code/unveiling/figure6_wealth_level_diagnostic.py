"""Exploratory Figure 6 diagnostic indexed by cohort mean wealth.

This module deliberately does not claim to reproduce Figure 6 of the July
2025 paper. It keeps the active-saving numerator reconstructed for Figure 5,
divides it by supplied fine-cohort pretax-income shares, and replaces the
percentile rank on the horizontal axis with mean real net wealth per adult.
The resulting repeated-cross-section diagnostic is useful for hypothesis
formation but cannot track the same households through time.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import numpy as np
import pandas as pd

from .figure5_authors import (
    ASSETS,
    ASSET_SHARE_CLASS,
    RESIDUAL_EQUITY_ASSETS,
    known_asset_inflation,
)
from .wealth_groups import (
    FINE_COHORT_LABELS,
    FINE_COHORT_POPULATION_SHARES,
    FINE_COHORTS,
    TOP_TEN_FINE_COHORTS,
)


DEFAULT_WINDOWS = {
    "pre_1982": (1963, 1982),
    "post_1982": (1983, 2016),
    "baseline_decade": (1973, 1982),
    "late_decade": (2007, 2016),
}


def load_demographics(path: Path) -> pd.DataFrame:
    """Load adult population and the national-income deflator.

    Parameters
    ----------
    path
        Authors-kit ``parameters_mss.csv`` file.

    Returns
    -------
    pandas.DataFrame
        One row per year for 1962--2016. ``totadults20`` is thousands of
        adults aged 20 or older and ``nideflator`` converts current dollars to
        2018 dollars.

    Raises
    ------
    ValueError
        If required columns, years, uniqueness, positivity, or finite-value
        assumptions fail.
    """

    required = {"yr", "totadults20", "nideflator"}
    frame = pd.read_csv(path, usecols=lambda column: column in required)
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"demographics: missing required columns {missing}")
    frame = frame.rename(columns={"yr": "year"})
    frame["year"] = pd.to_numeric(frame["year"], errors="raise")
    if not np.allclose(frame["year"], np.rint(frame["year"])):
        raise ValueError("demographics: year must contain integers")
    frame["year"] = np.rint(frame["year"]).astype(np.int16)
    frame = frame.loc[frame["year"].between(1962, 2016)].copy()
    if frame["year"].duplicated().any():
        raise ValueError("demographics: duplicate annual keys")
    numeric = ["totadults20", "nideflator"]
    frame[numeric] = frame[numeric].astype(np.float64)
    if not np.isfinite(frame[numeric].to_numpy()).all():
        raise ValueError("demographics: required values must be finite")
    if (frame[numeric] <= 0).any().any():
        raise ValueError("demographics: population and deflator must be positive")
    frame = frame.sort_values("year").reset_index(drop=True)
    expected_years = list(range(1962, 2017))
    if frame["year"].tolist() != expected_years:
        raise ValueError("demographics: expected complete 1962-2016 sample")
    return frame


def construct_fine_wealth_profiles(
    aggregate_wealth: pd.DataFrame,
    fine_shares: pd.DataFrame,
    valuation_inputs: pd.DataFrame,
    annual_saving: pd.DataFrame,
    demographics: pd.DataFrame,
) -> pd.DataFrame:
    """Construct annual active saving and mean wealth for each fine cohort.

    For fine cohort $c$ and balance-sheet category $j$, the implementation
    allocates the aggregate stock using the supplied DINA share,

    ``W[c,j,t] = W[j,t] * share[c,class(j),t]``,

    and applies active saving

    ``Theta[c,j,t] = W[c,j,t] - (1 + pi[c,j,t]) * W[c,j,t-1]``.

    The common residual equity return is inherited from the Figure 5 NIPA
    closure. Fine-cohort income is ``NatInc * szincsh[c]``. Mean wealth divides
    cohort net wealth by the estimated number of adults in the cohort and is
    reported in 2018 dollars.

    Returns
    -------
    pandas.DataFrame
        Long annual data for 1963--2016, keyed by ``(year, cohort)``.
        Monetary aggregates are current-dollar millions; mean wealth is real
        2018 dollars per adult; rates are decimal ratios.

    Raises
    ------
    ValueError
        If an annual merge loses observations, years are not contiguous, or
        wealth, saving, or income fails to aggregate to its supplied total.
    """

    frame = (
        aggregate_wealth.merge(
            fine_shares,
            on="year",
            how="inner",
            validate="one_to_one",
        )
        .merge(
            valuation_inputs,
            on="year",
            how="left",
            validate="one_to_one",
        )
        .merge(
            annual_saving[
                [
                    "year",
                    "private_saving_millions",
                    "residual_equity_inflation",
                ]
            ],
            on="year",
            how="left",
            validate="one_to_one",
        )
        .merge(
            demographics,
            on="year",
            how="inner",
            validate="one_to_one",
        )
        .sort_values("year")
        .reset_index(drop=True)
    )
    if len(frame) != len(aggregate_wealth):
        raise ValueError("fine profiles: annual merge lost observations")
    if not (frame["year"].diff().dropna() == 1).all():
        raise ValueError("fine profiles: years must be contiguous")
    required_annual = frame["year"].between(1963, 2016)
    required_values = [
        "JST_housing_capgain",
        "private_saving_millions",
        "residual_equity_inflation",
    ]
    if frame.loc[required_annual, required_values].isna().any().any():
        raise ValueError("fine profiles: missing valuation or saving inputs")

    records: list[pd.DataFrame] = []
    wealth_by_cohort: dict[str, pd.Series] = {}
    saving_by_cohort: dict[str, pd.Series] = {}
    income_by_cohort: dict[str, pd.Series] = {}
    for cohort_index, cohort in enumerate(FINE_COHORTS):
        wealth_components: list[pd.Series] = []
        saving_components: list[pd.Series] = []
        for asset, share_class in ASSET_SHARE_CLASS.items():
            level = (
                frame[f"h{asset}all"] * frame[f"sz{share_class}sh{cohort}"]
            )
            if asset in RESIDUAL_EQUITY_ASSETS:
                inflation = frame["residual_equity_inflation"]
            else:
                inflation = known_asset_inflation(
                    frame,
                    asset=asset,
                    use_top_ten_write_down=cohort in TOP_TEN_FINE_COHORTS,
                )
            wealth_components.append(level)
            saving_components.append(level - (1.0 + inflation) * level.shift(1))

        cohort_wealth = sum(wealth_components)
        cohort_saving = sum(saving_components)
        cohort_income = frame["NatInc"] * frame[f"szincsh{cohort}"]
        population_share = FINE_COHORT_POPULATION_SHARES[cohort]
        adults_thousands = frame["totadults20"] * population_share
        real_wealth_per_adult = (
            cohort_wealth / adults_thousands * frame["nideflator"] * 1_000.0
        )
        wealth_by_cohort[cohort] = cohort_wealth
        saving_by_cohort[cohort] = cohort_saving
        income_by_cohort[cohort] = cohort_income
        records.append(
            pd.DataFrame(
                {
                    "year": frame["year"],
                    "cohort": cohort,
                    "cohort_order": cohort_index,
                    "cohort_label": FINE_COHORT_LABELS[cohort],
                    "population_share": population_share,
                    "wealth_millions": cohort_wealth,
                    "real_mean_wealth_per_adult_2018_usd": (
                        real_wealth_per_adult
                    ),
                    "active_saving_millions": cohort_saving,
                    "pretax_income_millions": cohort_income,
                    "active_saving_to_pretax_income": (
                        cohort_saving / cohort_income
                    ),
                }
            )
        )

    _validate_fine_aggregation(
        frame,
        wealth_by_cohort=wealth_by_cohort,
        saving_by_cohort=saving_by_cohort,
        income_by_cohort=income_by_cohort,
    )
    output = pd.concat(records, ignore_index=True)
    output = output.loc[output["year"].between(1963, 2016)].copy()
    output = output.sort_values(["year", "cohort_order"]).reset_index(drop=True)
    if output.duplicated(["year", "cohort"]).any():
        raise ValueError("fine profiles: duplicate year/cohort keys")
    if not np.isfinite(
        output[
            [
                "real_mean_wealth_per_adult_2018_usd",
                "active_saving_millions",
                "pretax_income_millions",
                "active_saving_to_pretax_income",
            ]
        ].to_numpy()
    ).all():
        raise ValueError("fine profiles: non-finite output values")
    return output


def _validate_fine_aggregation(
    frame: pd.DataFrame,
    *,
    wealth_by_cohort: Mapping[str, pd.Series],
    saving_by_cohort: Mapping[str, pd.Series],
    income_by_cohort: Mapping[str, pd.Series],
) -> None:
    """Verify the three accounting totals behind the diagnostic."""

    aggregate_net_wealth = sum(frame[f"h{asset}all"] for asset in ASSETS)
    reconstructed_wealth = sum(wealth_by_cohort.values())
    wealth_scale = aggregate_net_wealth.abs().clip(lower=1.0)
    wealth_error = (
        (reconstructed_wealth - aggregate_net_wealth).abs() / wealth_scale
    )
    if wealth_error.max() > 2e-6:
        raise ValueError("fine profiles: wealth does not aggregate to supplied total")

    reconstructed_income = sum(income_by_cohort.values())
    income_error = (reconstructed_income - frame["NatInc"]).abs()
    income_scale = frame["NatInc"].abs().clip(lower=1.0)
    if (income_error / income_scale).max() > 2e-6:
        raise ValueError("fine profiles: income shares do not aggregate to total")

    reconstructed_saving = sum(saving_by_cohort.values())
    valid = frame["year"].between(1963, 2016)
    saving_error = (
        reconstructed_saving.loc[valid]
        - frame.loc[valid, "private_saving_millions"]
    ).abs()
    if (saving_error / income_scale.loc[valid]).max() > 1e-10:
        raise ValueError("fine profiles: saving does not satisfy NIPA closure")


def summarize_wealth_windows(
    profiles: pd.DataFrame,
    *,
    windows: Mapping[str, tuple[int, int]] = DEFAULT_WINDOWS,
) -> pd.DataFrame:
    """Pool fine-cohort profiles over named comparison windows.

    Saving rates are ratios of period sums, so a year with tiny cohort income
    cannot dominate through an unstable annual ratio. Mean real wealth gives
    each year equal weight within the window.
    """

    records: list[dict[str, float | int | str]] = []
    for window, (start_year, end_year) in windows.items():
        if start_year > end_year:
            raise ValueError(f"wealth windows: invalid range for {window}")
        expected_years = end_year - start_year + 1
        selected = profiles.loc[profiles["year"].between(start_year, end_year)]
        for cohort in FINE_COHORTS:
            cohort_data = selected.loc[selected["cohort"] == cohort]
            if len(cohort_data) != expected_years:
                raise ValueError(
                    f"wealth windows: {window}/{cohort} has {len(cohort_data)} "
                    f"years, expected {expected_years}"
                )
            income = cohort_data["pretax_income_millions"].sum()
            if income <= 0:
                raise ValueError(
                    f"wealth windows: {window}/{cohort} income must be positive"
                )
            records.append(
                {
                    "window": window,
                    "start_year": start_year,
                    "end_year": end_year,
                    "years": expected_years,
                    "cohort": cohort,
                    "cohort_order": int(cohort_data["cohort_order"].iloc[0]),
                    "cohort_label": FINE_COHORT_LABELS[cohort],
                    "population_share": FINE_COHORT_POPULATION_SHARES[cohort],
                    "real_mean_wealth_per_adult_2018_usd": cohort_data[
                        "real_mean_wealth_per_adult_2018_usd"
                    ].mean(),
                    "active_saving_millions": cohort_data[
                        "active_saving_millions"
                    ].sum(),
                    "pretax_income_millions": income,
                    "active_saving_to_pretax_income": (
                        cohort_data["active_saving_millions"].sum() / income
                    ),
                }
            )
    return pd.DataFrame(records).sort_values(
        ["start_year", "cohort_order"]
    ).reset_index(drop=True)
