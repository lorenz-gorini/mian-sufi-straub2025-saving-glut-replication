"""Reconstruct 2025 Figure 6 with February 2021 authors-kit inputs.

The target is the July 2025 net saving rate

``s_N[i,t] = Theta[i,t] / (Z_personal[i,t] + Z_corporate[i,t])``.

The module rebuilds the paper's bottom-40 and one-percentile wealth bins from
the supplied DINA microfile, applies the Figure 5 active-saving numerator, and
allocates personal and corporate disposable income consistently. The older
input vintage ends in 2016, so this is an exact-method old-input
reconstruction rather than an exact numerical reproduction of the 2019 paper
series.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path

import numpy as np
import pandas as pd

from .figure5_authors import (
    ASSETS,
    ASSET_SHARE_CLASS,
    DEBT_ASSETS,
    KNOWN_ASSETS,
    RESIDUAL_EQUITY_ASSETS,
)
from .wealth_groups import FINE_COHORTS


RAW_COLUMNS = (
    "year",
    "wealth_ptile",
    "dweght",
    "hwequ",
    "hwfix",
    "hwbus",
    "hwpen",
    "ownerhome",
    "ownermort",
    "nonmort",
    "taxbond",
    "currency",
    "muni",
    "poinc",
    "colexp",
    "govin",
    "prisupgov",
)

RAW_SHARE_CLASS_VARIABLE = {
    "equity": "hwequ",
    "pens": "hwpen",
    "bus": "hwbus",
    "ownerhome": "ownerhome",
    "ownermort": "ownermort",
    "nonmort": "nonmort",
    "taxbond": "taxbond",
    "currency": "currency",
    "muni": "muni",
    "fa": "fa",
    "ponog": "ponog",
}

SHARE_CLASSES = tuple(RAW_SHARE_CLASS_VARIABLE)
PERCENTILE_BINS = tuple(range(40, 101))
PAPER_WINDOWS = {
    "pre_1982": (1963, 1982),
    "post_1982": (1983, 2016),
}

PREPARED_FINE_VALIDATION_BINS = {
    "bottom_40": (range(40, 41), ("f10", "f20", "f30", "f35", "f40")),
    "p40_p45": (range(41, 46), ("f45",)),
    "p45_p50": (range(46, 51), ("f50",)),
    "p50_p55": (range(51, 56), ("f55",)),
    "p55_p60": (range(56, 61), ("f60",)),
    "p60_p65": (range(61, 66), ("f65",)),
    "p65_p70": (range(66, 71), ("f70",)),
    "p70_p75": (range(71, 76), ("f75",)),
    "p75_p80": (range(76, 81), ("f80",)),
    "p80_p85": (range(81, 86), ("f85",)),
    "p85_p90": (range(86, 91), ("f90",)),
    "p90_p95": (range(91, 96), ("f95",)),
    "p95_p99": (range(96, 100), ("f99",)),
    "top_1": (range(100, 101), ("f999", "f9999", "f99999", "f00001")),
}


def _normalize_year(series: pd.Series, *, label: str) -> pd.Series:
    """Return an integer calendar-year series from Stata year encodings."""

    if pd.api.types.is_datetime64_any_dtype(series):
        years = series.dt.year
    else:
        years = pd.to_numeric(series, errors="raise")
    if years.isna().any() or not np.allclose(years, np.rint(years)):
        raise ValueError(f"{label}: year must contain finite integers")
    return np.rint(years).astype(np.int16)


def collapse_percentile_share_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    """Collapse one DINA chunk into weighted year-percentile totals.

    The operation reproduces the relevant portion of the authors' Stata
    ``gcollapse`` step. ``dweght`` is stored as the population frequency weight
    times 100,000. Missing component values are treated as zero, matching
    Stata's sum behavior; year, percentile, and weight keys may not be missing.

    Parameters
    ----------
    chunk
        Raw DINA rows containing :data:`RAW_COLUMNS`.

    Returns
    -------
    pandas.DataFrame
        Weighted totals keyed by ``(year, percentile_bin)``. The bottom 40%
        forms one bin labelled 40; percentiles 41--100 remain separate.

    Raises
    ------
    ValueError
        If required columns or key/range assumptions fail.
    """

    missing = sorted(set(RAW_COLUMNS) - set(chunk.columns))
    if missing:
        raise ValueError(f"Figure 6 raw DINA chunk: missing columns {missing}")
    frame = chunk.loc[:, RAW_COLUMNS].copy()
    keys = ["year", "wealth_ptile", "dweght"]
    if frame[keys].isna().any().any():
        raise ValueError("Figure 6 raw DINA chunk: keys may not be missing")
    years = pd.to_numeric(frame["year"], errors="raise")
    percentiles = pd.to_numeric(frame["wealth_ptile"], errors="raise")
    if not np.allclose(years, np.rint(years)):
        raise ValueError("Figure 6 raw DINA chunk: year must be integer")
    if not np.allclose(percentiles, np.rint(percentiles)):
        raise ValueError("Figure 6 raw DINA chunk: percentile must be integer")
    frame["year"] = np.rint(years).astype(np.int16)
    frame["wealth_ptile"] = np.rint(percentiles).astype(np.int16)
    if not frame["year"].between(1962, 2016).all():
        raise ValueError("Figure 6 raw DINA chunk: year outside 1962-2016")
    if not frame["wealth_ptile"].between(1, 100).all():
        raise ValueError("Figure 6 raw DINA chunk: percentile outside 1-100")

    frequency_weight = np.floor(frame["dweght"] / 100_000.0 + 0.5)
    if (frequency_weight < 0).any() or not np.isfinite(frequency_weight).all():
        raise ValueError("Figure 6 raw DINA chunk: invalid frequency weight")
    frame["frequency_weight"] = frequency_weight.astype(np.float64)
    frame["percentile_bin"] = frame["wealth_ptile"].clip(lower=40)

    components = sorted(set(RAW_SHARE_CLASS_VARIABLE.values()) - {"fa", "ponog"})
    frame[components] = frame[components].astype(np.float64).fillna(0.0)
    frame["fa"] = frame[["hwequ", "hwfix", "hwbus", "hwpen"]].sum(axis=1)
    disposable_components = ["poinc", "colexp", "govin", "prisupgov"]
    frame[disposable_components] = (
        frame[disposable_components].astype(np.float64).fillna(0.0)
    )
    frame["ponog"] = (
        frame["poinc"]
        - frame["colexp"]
        - frame["govin"]
        - frame["prisupgov"]
    )
    value_columns = list(RAW_SHARE_CLASS_VARIABLE.values())
    weighted = frame[value_columns].multiply(
        frame["frequency_weight"],
        axis=0,
    )
    weighted["population_weight"] = frame["frequency_weight"]
    weighted["year"] = frame["year"]
    weighted["percentile_bin"] = frame["percentile_bin"]
    return weighted.groupby(
        ["year", "percentile_bin"],
        observed=True,
        sort=True,
    ).sum()


def build_percentile_shares(
    path: Path,
    *,
    chunksize: int = 250_000,
    progress: Callable[[int], None] | None = None,
) -> pd.DataFrame:
    """Scan the raw DINA file and construct Figure 6 percentile-bin shares.

    Parameters
    ----------
    path
        Authors-kit ``usdina19622016.dta`` path.
    chunksize
        Rows processed at a time. This bounds memory use for the 16 GB source.
    progress
        Optional callback receiving the cumulative number of processed rows.

    Returns
    -------
    pandas.DataFrame
        One row per year and paper percentile bin for 1962--2016. Each
        ``share_*`` column and ``population_share`` sum to one within year.
    """

    if chunksize <= 0:
        raise ValueError("Figure 6 percentile shares: chunksize must be positive")
    reader = pd.read_stata(
        path,
        columns=list(RAW_COLUMNS),
        convert_categoricals=False,
        iterator=True,
        chunksize=chunksize,
    )
    totals: pd.DataFrame | None = None
    rows_processed = 0
    for chunk in reader:
        collapsed = collapse_percentile_share_chunk(chunk)
        totals = (
            collapsed
            if totals is None
            else totals.add(collapsed, fill_value=0.0)
        )
        rows_processed += len(chunk)
        if progress is not None:
            progress(rows_processed)
    if totals is None or rows_processed == 0:
        raise ValueError("Figure 6 percentile shares: raw file contains no rows")
    return normalize_percentile_totals(totals.reset_index())


def normalize_percentile_totals(totals: pd.DataFrame) -> pd.DataFrame:
    """Normalize collapsed values into annual shares and fill missing years."""

    value_columns = [*RAW_SHARE_CLASS_VARIABLE.values(), "population_weight"]
    required = {"year", "percentile_bin", *value_columns}
    missing = sorted(required - set(totals.columns))
    if missing:
        raise ValueError(f"Figure 6 percentile totals: missing columns {missing}")
    frame = totals.copy()
    if frame.duplicated(["year", "percentile_bin"]).any():
        raise ValueError("Figure 6 percentile totals: duplicate keys")
    if not frame["percentile_bin"].isin(PERCENTILE_BINS).all():
        raise ValueError("Figure 6 percentile totals: unexpected percentile bin")
    observed_years = set(pd.to_numeric(frame["year"], errors="raise").astype(int))
    expected_observed_years = set(range(1962, 2017)) - {1963, 1965}
    if observed_years != expected_observed_years:
        missing_years = sorted(expected_observed_years - observed_years)
        extra_years = sorted(observed_years - expected_observed_years)
        raise ValueError(
            "Figure 6 percentile totals: unexpected raw-year coverage; "
            f"missing={missing_years}, extra={extra_years}"
        )

    output = frame[["year", "percentile_bin"]].copy()
    for share_class, source in RAW_SHARE_CLASS_VARIABLE.items():
        denominator = frame.groupby("year")[source].transform("sum")
        if (denominator == 0).any():
            raise ValueError(
                f"Figure 6 percentile totals: zero {share_class} denominator"
            )
        output[f"share_{share_class}"] = frame[source] / denominator
    population_total = frame.groupby("year")["population_weight"].transform("sum")
    output["population_share"] = frame["population_weight"] / population_total

    full_index = pd.MultiIndex.from_product(
        [range(1962, 2017), PERCENTILE_BINS],
        names=["year", "percentile_bin"],
    )
    output = output.set_index(["year", "percentile_bin"]).reindex(full_index)
    share_columns = [f"share_{name}" for name in SHARE_CLASSES]
    fill_columns = [*share_columns, "population_share"]
    output[fill_columns] = output.groupby(
        level="percentile_bin",
        group_keys=False,
    )[fill_columns].apply(lambda group: group.interpolate(limit_direction="both"))
    if output[fill_columns].isna().any().any():
        raise ValueError("Figure 6 percentile shares: unresolved missing years")
    output = output.reset_index()

    for column in fill_columns:
        annual_error = (output.groupby("year")[column].sum() - 1.0).abs()
        if annual_error.max() > 2e-8:
            raise ValueError(
                f"Figure 6 percentile shares: {column} does not sum to one; "
                f"max error={annual_error.max():.3g}"
            )
    output["bin_label"] = output["percentile_bin"].map(_percentile_bin_label)
    output["uses_top_ten_debt_return"] = output["percentile_bin"] > 90
    return output.sort_values(["year", "percentile_bin"]).reset_index(drop=True)


def validate_against_prepared_fine_shares(
    percentile_shares: pd.DataFrame,
    prepared_path: Path,
    *,
    tolerance: float = 1e-6,
) -> pd.DataFrame:
    """Validate the raw reconstruction against the authors' prepared shares.

    The prepared file is too coarse to validate every one-percentile bin, but
    it independently checks all aggregations available from the bottom 40%
    through the top 1%. The function returns one summary row per share class
    and raises if any cell differs by more than ``tolerance``.

    Parameters
    ----------
    percentile_shares
        Long raw reconstruction keyed by year and paper percentile bin.
    prepared_path
        Authors-kit ``Yszshares_fine.dta`` path.
    tolerance
        Maximum allowed absolute share discrepancy.

    Returns
    -------
    pandas.DataFrame
        Maximum and mean absolute discrepancies by share class, including the
        year and validation bin at which the maximum occurs.
    """

    if tolerance <= 0:
        raise ValueError("Figure 6 share validation: tolerance must be positive")
    required = {
        "year",
        "percentile_bin",
        *(f"share_{share_class}" for share_class in SHARE_CLASSES),
    }
    missing = sorted(required - set(percentile_shares.columns))
    if missing:
        raise ValueError(f"Figure 6 share validation: missing columns {missing}")

    prepared_columns = [
        "year",
        *(
            f"sz{share_class}sh{cohort}"
            for share_class in SHARE_CLASSES
            for cohort in FINE_COHORTS
        ),
    ]
    prepared = pd.read_stata(
        prepared_path,
        columns=prepared_columns,
        convert_categoricals=False,
    )
    prepared["year"] = _normalize_year(
        prepared["year"],
        label="prepared fine-share validation",
    )
    if prepared["year"].duplicated().any():
        raise ValueError("Figure 6 share validation: duplicate prepared years")

    comparison_records: list[dict[str, float | int | str]] = []
    for label, (percentile_bins, fine_cohorts) in (
        PREPARED_FINE_VALIDATION_BINS.items()
    ):
        reconstructed = percentile_shares.loc[
            percentile_shares["percentile_bin"].isin(percentile_bins)
        ].groupby("year")
        for share_class in SHARE_CLASSES:
            raw_share = reconstructed[f"share_{share_class}"].sum()
            prepared_share = prepared.set_index("year")[
                [f"sz{share_class}sh{cohort}" for cohort in fine_cohorts]
            ].sum(axis=1)
            aligned = pd.concat(
                [
                    raw_share.rename("raw_share"),
                    prepared_share.rename("prepared_share"),
                ],
                axis=1,
                join="inner",
            )
            for year, row in aligned.iterrows():
                comparison_records.append(
                    {
                        "share_class": share_class,
                        "validation_bin": label,
                        "year": int(year),
                        "raw_share": float(row["raw_share"]),
                        "prepared_share": float(row["prepared_share"]),
                        "absolute_error": abs(
                            float(row["raw_share"] - row["prepared_share"])
                        ),
                    }
                )
    comparison = pd.DataFrame(comparison_records)
    if comparison.empty:
        raise ValueError("Figure 6 share validation: no comparable cells")
    worst_index = comparison.groupby("share_class")["absolute_error"].idxmax()
    summary = comparison.loc[worst_index].copy()
    mean_errors = comparison.groupby("share_class")["absolute_error"].mean()
    summary["mean_absolute_error"] = summary["share_class"].map(mean_errors)
    summary = summary.rename(columns={"absolute_error": "max_absolute_error"})
    summary = summary[
        [
            "share_class",
            "max_absolute_error",
            "mean_absolute_error",
            "year",
            "validation_bin",
            "raw_share",
            "prepared_share",
        ]
    ].sort_values("share_class").reset_index(drop=True)
    if summary["max_absolute_error"].max() > tolerance:
        worst = summary.loc[summary["max_absolute_error"].idxmax()]
        raise ValueError(
            "Figure 6 share validation failed: "
            f"{worst['share_class']} max error "
            f"{worst['max_absolute_error']:.3g} exceeds {tolerance:.3g}"
        )
    return summary


def _percentile_bin_label(percentile_bin: int) -> str:
    """Return a readable label for one paper percentile bin."""

    if percentile_bin == 40:
        return "Bottom 40%"
    if percentile_bin == 100:
        return "Top 1%"
    return f"{percentile_bin - 1}–{percentile_bin}%"


def load_percentile_shares(path: Path) -> pd.DataFrame:
    """Load and validate a generated Figure 6 percentile-share file."""

    frame = pd.read_csv(path)
    required = {
        "year",
        "percentile_bin",
        "bin_label",
        "population_share",
        "uses_top_ten_debt_return",
        *(f"share_{name}" for name in SHARE_CLASSES),
    }
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Figure 6 percentile shares: missing columns {missing}")
    if frame.duplicated(["year", "percentile_bin"]).any():
        raise ValueError("Figure 6 percentile shares: duplicate keys")
    expected_rows = 55 * len(PERCENTILE_BINS)
    if len(frame) != expected_rows:
        raise ValueError(
            f"Figure 6 percentile shares: expected {expected_rows} rows, "
            f"found {len(frame)}"
        )
    frame["uses_top_ten_debt_return"] = frame[
        "uses_top_ten_debt_return"
    ].map({True: True, False: False, "True": True, "False": False})
    if frame["uses_top_ten_debt_return"].isna().any():
        raise ValueError("Figure 6 percentile shares: invalid debt-return flag")
    return frame.sort_values(["year", "percentile_bin"]).reset_index(drop=True)


def load_disposable_income_inputs(
    wealth_path: Path,
    nipa_path: Path,
) -> pd.DataFrame:
    """Load aggregate personal and corporate disposable income.

    ``szponog`` is the kit's personal disposable-income concept excluding
    government collective consumption. Following the 2025 paper, business
    saving is corporate disposable income attributable to private households.
    Both supplied series are billions of current dollars and are converted to
    millions.
    """

    personal = pd.read_stata(
        wealth_path,
        columns=["year", "szponog"],
        convert_categoricals=False,
    )
    corporate = pd.read_stata(
        nipa_path,
        columns=["year", "SavingBus"],
        convert_categoricals=False,
    )
    personal["year"] = _normalize_year(personal["year"], label="personal disposable")
    corporate["year"] = _normalize_year(
        corporate["year"],
        label="corporate disposable",
    )
    frame = personal.merge(
        corporate,
        on="year",
        how="inner",
        validate="one_to_one",
    )
    frame = frame.loc[frame["year"].between(1962, 2016)].copy()
    if frame["year"].tolist() != list(range(1962, 2017)):
        raise ValueError("Figure 6 disposable income: expected 1962-2016")
    frame["personal_disposable_income_millions"] = frame["szponog"] * 1_000.0
    frame["corporate_disposable_income_millions"] = (
        frame["SavingBus"] * 1_000.0
    )
    required = [
        "personal_disposable_income_millions",
        "corporate_disposable_income_millions",
    ]
    if not np.isfinite(frame[required].to_numpy()).all():
        raise ValueError("Figure 6 disposable income: non-finite values")
    if (frame[required] <= 0).any().any():
        raise ValueError("Figure 6 disposable income: values must be positive")
    return frame[["year", *required]].reset_index(drop=True)


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
    """

    required = {"yr", "totadults20", "nideflator"}
    frame = pd.read_csv(path, usecols=lambda column: column in required)
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"demographics: missing required columns {missing}")
    frame = frame.rename(columns={"yr": "year"})
    frame["year"] = _normalize_year(frame["year"], label="demographics")
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
    if frame["year"].tolist() != list(range(1962, 2017)):
        raise ValueError("demographics: expected complete 1962-2016 sample")
    return frame


def construct_annual_percentile_profiles(
    aggregate_wealth: pd.DataFrame,
    percentile_shares: pd.DataFrame,
    valuation_inputs: pd.DataFrame,
    annual_saving: pd.DataFrame,
    disposable_income: pd.DataFrame,
    demographics: pd.DataFrame,
) -> pd.DataFrame:
    """Construct annual Figure 6 saving rates for the paper percentile bins.

    The active-saving numerator is identical to the Figure 5 reconstruction.
    Personal disposable income is allocated with ``ponog`` shares and
    corporate disposable income with corporate-equity shares, following the
    paper's equations (8c) and (9c).

    Returns
    -------
    pandas.DataFrame
        Annual 1963--2016 observations keyed by year and percentile bin.
        Stocks and flows are current-dollar millions, real wealth is 2018
        dollars per adult, and the saving rate is a decimal ratio.
    """

    frame = (
        percentile_shares.merge(
            aggregate_wealth,
            on="year",
            how="inner",
            validate="many_to_one",
        )
        .merge(
            valuation_inputs,
            on="year",
            how="left",
            validate="many_to_one",
        )
        .merge(
            annual_saving[
                [
                    "year",
                    "private_saving_millions",
                ]
            ],
            on="year",
            how="left",
            validate="many_to_one",
        )
        .merge(
            disposable_income,
            on="year",
            how="inner",
            validate="many_to_one",
        )
        .merge(
            demographics,
            on="year",
            how="inner",
            validate="many_to_one",
        )
        .sort_values(["percentile_bin", "year"])
        .reset_index(drop=True)
    )
    if len(frame) != len(percentile_shares):
        raise ValueError("Figure 6 profiles: annual merge lost observations")
    required_years = frame["year"].between(1963, 2016)
    needed = [
        "JST_housing_capgain",
        "private_saving_millions",
    ]
    if frame.loc[required_years, needed].isna().any().any():
        raise ValueError("Figure 6 profiles: missing valuation or saving input")

    net_wealth = pd.Series(0.0, index=frame.index)
    levels: dict[str, pd.Series] = {}
    for asset, share_class in ASSET_SHARE_CLASS.items():
        level = frame[f"h{asset}all"] * frame[f"share_{share_class}"]
        levels[asset] = level
        net_wealth += level

    active_saving = pd.Series(0.0, index=frame.index)
    for asset in KNOWN_ASSETS:
        level = levels[asset]
        previous = level.groupby(frame["percentile_bin"]).shift(1)
        inflation = _known_percentile_asset_inflation(frame, asset=asset)
        active_saving += level - (1.0 + inflation) * previous

    known_saving = active_saving.groupby(frame["year"]).sum(min_count=1)
    annual_private_saving = annual_saving.set_index("year")[
        "private_saving_millions"
    ]
    equity_current = sum(
        aggregate_wealth.set_index("year")[f"h{asset}all"]
        for asset in RESIDUAL_EQUITY_ASSETS
    )
    residual_saving = annual_private_saving - known_saving
    residual_equity_inflation = (
        (equity_current - residual_saving) / equity_current.shift(1) - 1.0
    )
    frame["figure6_residual_equity_inflation"] = frame["year"].map(
        residual_equity_inflation
    )
    for asset in RESIDUAL_EQUITY_ASSETS:
        level = levels[asset]
        previous = level.groupby(frame["percentile_bin"]).shift(1)
        active_saving += level - (
            1.0 + frame["figure6_residual_equity_inflation"]
        ) * previous

    frame["wealth_millions"] = net_wealth
    frame["active_saving_millions"] = active_saving
    frame["personal_disposable_income_millions"] *= frame["share_ponog"]
    frame["corporate_disposable_income_millions"] *= frame["share_equity"]
    frame["total_disposable_income_millions"] = (
        frame["personal_disposable_income_millions"]
        + frame["corporate_disposable_income_millions"]
    )
    if (frame.loc[required_years, "total_disposable_income_millions"] <= 0).any():
        raise ValueError("Figure 6 profiles: disposable income must be positive")
    frame["net_saving_rate"] = (
        frame["active_saving_millions"]
        / frame["total_disposable_income_millions"]
    )
    adults_thousands = frame["totadults20"] * frame["population_share"]
    frame["real_mean_wealth_per_adult_2018_usd"] = (
        frame["wealth_millions"]
        / adults_thousands
        * frame["nideflator"]
        * 1_000.0
    )

    _validate_annual_profiles(frame, aggregate_wealth, annual_saving, disposable_income)
    output_columns = [
        "year",
        "percentile_bin",
        "bin_label",
        "population_share",
        "wealth_millions",
        "real_mean_wealth_per_adult_2018_usd",
        "active_saving_millions",
        "personal_disposable_income_millions",
        "corporate_disposable_income_millions",
        "total_disposable_income_millions",
        "net_saving_rate",
    ]
    output = frame.loc[required_years, output_columns].copy()
    output = output.sort_values(["year", "percentile_bin"]).reset_index(drop=True)
    if not np.isfinite(output.select_dtypes(include=np.number).to_numpy()).all():
        raise ValueError("Figure 6 profiles: non-finite output values")
    return output


def _known_percentile_asset_inflation(
    frame: pd.DataFrame,
    *,
    asset: str,
) -> pd.Series:
    """Return annual valuation factors for all percentile bins."""

    if asset not in KNOWN_ASSETS:
        raise ValueError(f"Figure 6 profiles: {asset} has residual inflation")
    if asset == "arealest":
        return frame["JST_housing_capgain"]
    if asset not in DEBT_ASSETS:
        return pd.Series(0.0, index=frame.index)
    debt_type = "mdebt" if asset == "lhommort" else "cdebt"
    top = frame[f"ZIP_{debt_type}_wd10"].fillna(0.0)
    bottom = frame[f"ZIP_{debt_type}_wd90"].fillna(0.0)
    write_down = np.where(frame["uses_top_ten_debt_return"], top, bottom)
    return pd.Series(-write_down, index=frame.index)


def _validate_annual_profiles(
    frame: pd.DataFrame,
    aggregate_wealth: pd.DataFrame,
    annual_saving: pd.DataFrame,
    disposable_income: pd.DataFrame,
) -> None:
    """Verify wealth, saving, disposable-income, and equation (9c) closure."""

    valid = frame["year"].between(1963, 2016)
    grouped = frame.loc[valid].groupby("year")
    years = grouped.size().index

    aggregate = aggregate_wealth.set_index("year").loc[years]
    expected_wealth = sum(aggregate[f"h{asset}all"] for asset in ASSETS)
    wealth_error = (grouped["wealth_millions"].sum() - expected_wealth).abs()
    if (wealth_error / expected_wealth.abs().clip(lower=1.0)).max() > 2e-8:
        raise ValueError("Figure 6 profiles: aggregate wealth closure failed")

    saving_expected = annual_saving.set_index("year").loc[
        years,
        "private_saving_millions",
    ]
    saving_rebuilt = grouped["active_saving_millions"].sum()
    scale = aggregate["NatInc"].abs().clip(lower=1.0)
    saving_relative_error = (saving_rebuilt - saving_expected).abs() / scale
    if saving_relative_error.max() > 1e-10:
        raise ValueError(
            "Figure 6 profiles: NIPA saving closure failed; "
            f"max error={saving_relative_error.max():.3g} of national income"
        )

    income = disposable_income.set_index("year").loc[years]
    personal_error = (
        grouped["personal_disposable_income_millions"].sum()
        - income["personal_disposable_income_millions"]
    ).abs()
    corporate_error = (
        grouped["corporate_disposable_income_millions"].sum()
        - income["corporate_disposable_income_millions"]
    ).abs()
    if (personal_error / scale).max() > 2e-8:
        raise ValueError("Figure 6 profiles: personal-income closure failed")
    if (corporate_error / scale).max() > 2e-8:
        raise ValueError("Figure 6 profiles: corporate-income closure failed")

    equation_9c = grouped.apply(
        lambda group: (
            group["net_saving_rate"]
            * group["total_disposable_income_millions"]
        ).sum(),
        include_groups=False,
    )
    if ((equation_9c - saving_expected).abs() / scale).max() > 1e-10:
        raise ValueError("Figure 6 profiles: equation (9c) closure failed")


def summarize_period_profiles(
    annual_profiles: pd.DataFrame,
    *,
    windows: Mapping[str, tuple[int, int]] = PAPER_WINDOWS,
) -> pd.DataFrame:
    """Average annual Figure 6 rates within the paper comparison periods.

    The main rate is the simple mean of annual cohort rates, matching the old
    authors-code ``tabstat, statistics(mean)`` convention. A pooled ratio of
    period sums is retained as a diagnostic.
    """

    records: list[dict[str, float | int | str]] = []
    for window, (start_year, end_year) in windows.items():
        if start_year > end_year:
            raise ValueError(f"Figure 6 windows: invalid range for {window}")
        expected_years = end_year - start_year + 1
        selected = annual_profiles.loc[
            annual_profiles["year"].between(start_year, end_year)
        ]
        for percentile_bin in PERCENTILE_BINS:
            cohort = selected.loc[
                selected["percentile_bin"] == percentile_bin
            ]
            if len(cohort) != expected_years:
                raise ValueError(
                    f"Figure 6 windows: {window}/{percentile_bin} has "
                    f"{len(cohort)} years, expected {expected_years}"
                )
            disposable = cohort["total_disposable_income_millions"].sum()
            records.append(
                {
                    "window": window,
                    "start_year": start_year,
                    "end_year": end_year,
                    "years": expected_years,
                    "percentile_bin": percentile_bin,
                    "bin_label": cohort["bin_label"].iloc[0],
                    "mean_annual_net_saving_rate": cohort[
                        "net_saving_rate"
                    ].mean(),
                    "pooled_net_saving_rate": (
                        cohort["active_saving_millions"].sum() / disposable
                    ),
                    "real_mean_wealth_per_adult_2018_usd": cohort[
                        "real_mean_wealth_per_adult_2018_usd"
                    ].mean(),
                }
            )
    return pd.DataFrame(records).sort_values(
        ["start_year", "percentile_bin"]
    ).reset_index(drop=True)


def build_rolling_profiles(
    annual_profiles: pd.DataFrame,
    *,
    window_years: int = 5,
) -> pd.DataFrame:
    """Average annual Figure 6 rates over trailing multi-year windows.

    The statistic preserves the paper's convention of averaging annual saving
    rates rather than pooling saving and income across years. A five-year
    window makes medium-run movement visible without treating one noisy annual
    observation as a structural change.

    Parameters
    ----------
    annual_profiles
        Validated annual Figure 6 output keyed by year and percentile bin.
    window_years
        Number of consecutive annual rates in each trailing window.

    Returns
    -------
    pandas.DataFrame
        One row per window-end year and percentile bin. Rates are decimal
        ratios; ``window_start_year`` and ``window_end_year`` are inclusive.

    Raises
    ------
    ValueError
        If the window is invalid or any percentile series is not annual and
        contiguous.
    """

    if window_years < 2:
        raise ValueError("Figure 6 rolling profiles: window must be at least 2")
    required = {"year", "percentile_bin", "bin_label", "net_saving_rate"}
    missing = sorted(required - set(annual_profiles.columns))
    if missing:
        raise ValueError(f"Figure 6 rolling profiles: missing columns {missing}")
    frame = annual_profiles[
        ["year", "percentile_bin", "bin_label", "net_saving_rate"]
    ].copy()
    if frame.duplicated(["year", "percentile_bin"]).any():
        raise ValueError("Figure 6 rolling profiles: duplicate annual keys")
    frame = frame.sort_values(["percentile_bin", "year"]).reset_index(drop=True)
    for percentile_bin, cohort in frame.groupby("percentile_bin"):
        if not (cohort["year"].diff().dropna() == 1).all():
            raise ValueError(
                "Figure 6 rolling profiles: non-contiguous years for "
                f"percentile {percentile_bin}"
            )
        if len(cohort) < window_years:
            raise ValueError(
                "Figure 6 rolling profiles: insufficient years for "
                f"percentile {percentile_bin}"
            )
    frame["rolling_mean_net_saving_rate"] = frame.groupby(
        "percentile_bin"
    )["net_saving_rate"].transform(
        lambda series: series.rolling(
            window=window_years,
            min_periods=window_years,
        ).mean()
    )
    frame = frame.dropna(subset=["rolling_mean_net_saving_rate"]).copy()
    frame["window_years"] = window_years
    frame["window_end_year"] = frame["year"]
    frame["window_start_year"] = frame["year"] - window_years + 1
    return frame[
        [
            "window_start_year",
            "window_end_year",
            "window_years",
            "percentile_bin",
            "bin_label",
            "rolling_mean_net_saving_rate",
        ]
    ].reset_index(drop=True)


def build_paper_comparison(
    period_profiles: pd.DataFrame,
    paper_profiles: pd.DataFrame,
) -> pd.DataFrame:
    """Align old-input reconstruction and digitized 2025 Figure 6 curves."""

    ours = period_profiles.pivot(
        index="percentile_bin",
        columns="window",
        values="mean_annual_net_saving_rate",
    ).reset_index()
    ours = ours.rename(
        columns={
            "pre_1982": "authors_pre_1982_rate",
            "post_1982": "authors_post_1982_rate",
        }
    )
    output = paper_profiles.merge(
        ours,
        left_on="wealth_percentile",
        right_on="percentile_bin",
        how="inner",
        validate="one_to_one",
    ).drop(columns="percentile_bin")
    for period in ("pre_1982", "post_1982"):
        output[f"error_{period}"] = (
            output[f"authors_{period}_rate"]
            - output[f"paper_{period}_rate"]
        )
    return output
