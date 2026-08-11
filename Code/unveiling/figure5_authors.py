"""Reconstruct 2025 Figure 5 from February 2021 authors-kit inputs.

The module starts from the authors' prepared aggregate wealth levels,
fine-cohort DINA shares, valuation inputs, and NIPA saving totals.  It
reimplements the active-saving identity and the residual equity-valuation
closure before applying the July 2025 display transformation.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .wealth_groups import FINE_COHORTS, WEALTH_GROUP_COHORTS


ASSET_SHARE_CLASS = {
    "arealest": "ownerhome",
    "aforedep": "taxbond",
    "ackdpcur": "currency",
    "atisadep": "taxbond",
    "amonmark": "taxbond",
    "ammfmuni": "muni",
    "atreasur": "taxbond",
    "aagengse": "taxbond",
    "amunisec": "muni",
    "acrfrbnd": "taxbond",
    "aloanadv": "taxbond",
    "amrtcred": "taxbond",
    "acorpequ": "equity",
    "amufuequ": "equity",
    "amufubnd": "taxbond",
    "amufumun": "muni",
    "alinsequ": "pens",
    "alinsfix": "pens",
    "apensequ": "pens",
    "apensfix": "pens",
    "apiraequ": "pens",
    "apirafix": "pens",
    "ancrpequ": "bus",
    "amiscell": "fa",
    "lhommort": "ownermort",
    "lcnscred": "nonmort",
    "ldplnnec": "nonmort",
    "lothloan": "nonmort",
    "ldulifin": "nonmort",
}

ASSETS = tuple(ASSET_SHARE_CLASS)
RESIDUAL_EQUITY_ASSETS = (
    "acorpequ",
    "amufuequ",
    "alinsequ",
    "apensequ",
    "apiraequ",
    "ancrpequ",
    "amiscell",
)
KNOWN_ASSETS = tuple(
    asset for asset in ASSETS if asset not in RESIDUAL_EQUITY_ASSETS
)
DEBT_ASSETS = (
    "lhommort",
    "lcnscred",
    "ldplnnec",
    "lothloan",
    "ldulifin",
)
GROUPS = tuple(WEALTH_GROUP_COHORTS)


def _normalize_year(series: pd.Series, *, label: str) -> pd.Series:
    """Return an integer calendar-year series from Stata year encodings."""

    if pd.api.types.is_datetime64_any_dtype(series):
        years = series.dt.year
    else:
        years = pd.to_numeric(series, errors="raise")
    if years.isna().any() or not np.allclose(years, np.rint(years)):
        raise ValueError(f"{label}: year must contain finite integers")
    return np.rint(years).astype(np.int16)


def _validate_annual_frame(
    frame: pd.DataFrame,
    *,
    label: str,
    required_columns: set[str],
) -> pd.DataFrame:
    """Validate columns, annual key uniqueness, ordering, and finiteness."""

    missing = sorted(required_columns - set(frame.columns))
    if missing:
        raise ValueError(f"{label}: missing required columns {missing}")
    output = frame.copy()
    output["year"] = _normalize_year(output["year"], label=label)
    if output["year"].duplicated().any():
        duplicates = output.loc[output["year"].duplicated(), "year"].tolist()
        raise ValueError(f"{label}: duplicate annual keys {duplicates}")
    output = output.sort_values("year").reset_index(drop=True)
    numeric_columns = list(required_columns - {"year"})
    output[numeric_columns] = output[numeric_columns].astype(np.float64)
    values = output[numeric_columns]
    if not np.isfinite(values.to_numpy(dtype=float)).all():
        raise ValueError(f"{label}: required values must be finite")
    return output


def load_aggregate_wealth(path: Path) -> pd.DataFrame:
    """Load aggregate asset levels and national income from ``YwealthFOF``.

    Returns
    -------
    pandas.DataFrame
        One row per year. Monetary values are millions of current dollars.
    """

    columns = ["year", "NatInc", *(f"h{asset}all" for asset in ASSETS)]
    frame = pd.read_stata(path, columns=columns, convert_categoricals=False)
    frame = frame.loc[pd.to_numeric(frame["year"]).between(1962, 2016)]
    return _validate_annual_frame(
        frame,
        label="aggregate wealth",
        required_columns=set(columns),
    )


def load_fine_wealth_shares(path: Path) -> pd.DataFrame:
    """Load fine DINA wealth and income shares.

    The income shares are not required by the Figure 5 aggregation itself,
    but retaining and validating them supports the adjacent wealth-level
    saving-rate diagnostic without loading the same source under a second
    schema.
    """

    share_classes = sorted({*ASSET_SHARE_CLASS.values(), "inc"})
    columns = [
        "year",
        *(
            f"sz{share_class}sh{cohort}"
            for share_class in share_classes
            for cohort in FINE_COHORTS
        ),
    ]
    frame = pd.read_stata(path, columns=columns, convert_categoricals=False)
    frame = _validate_annual_frame(
        frame,
        label="fine DINA shares",
        required_columns=set(columns),
    )
    for share_class in share_classes:
        class_columns = [
            f"sz{share_class}sh{cohort}" for cohort in FINE_COHORTS
        ]
        error = (frame[class_columns].sum(axis=1) - 1.0).abs()
        if error.max() > 2e-6:
            raise ValueError(
                f"fine DINA shares: {share_class} shares do not sum to one; "
                f"max error={error.max():.3g}"
            )
    return frame


def load_valuation_inputs(path: Path) -> pd.DataFrame:
    """Load supplied housing and cohort-specific debt write-down inputs."""

    columns = [
        "year",
        "JST_housing_capgain",
        "ZIP_cdebt_wd10",
        "ZIP_cdebt_wd90",
        "ZIP_mdebt_wd10",
        "ZIP_mdebt_wd90",
    ]
    frame = pd.read_stata(path, columns=columns, convert_categoricals=False)
    frame["year"] = _normalize_year(frame["year"], label="valuation inputs")
    if frame["year"].duplicated().any():
        raise ValueError("valuation inputs: duplicate annual keys")
    frame[columns[1:]] = frame[columns[1:]].astype(np.float64)
    return frame.sort_values("year").reset_index(drop=True)


def load_private_saving(path: Path) -> pd.DataFrame:
    """Load NIPA personal and business saving and convert to millions."""

    columns = ["year", "PersSaving", "SavingBus"]
    frame = pd.read_stata(path, columns=columns, convert_categoricals=False)
    frame = frame.loc[pd.to_numeric(frame["year"]).between(1962, 2016)]
    frame = _validate_annual_frame(
        frame,
        label="NIPA private saving",
        required_columns=set(columns),
    )
    frame["private_saving_millions"] = (
        frame["PersSaving"] + frame["SavingBus"]
    ) * 1_000.0
    return frame[["year", "private_saving_millions"]]


def load_saving_benchmark(path: Path) -> pd.DataFrame:
    """Load authors' final annual saving ratios for validation only."""

    columns = ["year", "saving_12NI", "saving_92NI", "saving_902NI"]
    frame = pd.read_stata(path, columns=columns, convert_categoricals=False)
    return _validate_annual_frame(
        frame,
        label="saving benchmark",
        required_columns=set(columns),
    )


def construct_group_wealth(
    aggregate_wealth: pd.DataFrame,
    fine_shares: pd.DataFrame,
) -> pd.DataFrame:
    """Allocate aggregate wealth levels to the paper's four wealth groups.

    The Financial Accounts determine each aggregate asset or liability level.
    Fine DINA shares determine its distribution across top 1%, next 9%, next
    40%, and bottom 50%. Liabilities retain the negative balance-sheet sign.
    """

    merged = aggregate_wealth.merge(
        fine_shares,
        on="year",
        how="inner",
        validate="one_to_one",
    )
    if len(merged) != len(aggregate_wealth) or len(merged) != len(fine_shares):
        raise ValueError("group wealth: annual merge lost observations")

    allocated: dict[str, pd.Series] = {
        "year": merged["year"],
        "NatInc": merged["NatInc"],
    }
    for asset, share_class in ASSET_SHARE_CLASS.items():
        grouped_levels: list[pd.Series] = []
        for group, cohorts in WEALTH_GROUP_COHORTS.items():
            share_columns = [
                f"sz{share_class}sh{cohort}" for cohort in cohorts
            ]
            level_column = f"h{asset}_{group}"
            allocated[level_column] = (
                merged[f"h{asset}all"] * merged[share_columns].sum(axis=1)
            )
            grouped_levels.append(allocated[level_column])
        reconstructed_total = pd.concat(grouped_levels, axis=1).sum(axis=1)
        error = (reconstructed_total - merged[f"h{asset}all"]).abs()
        scale = merged[f"h{asset}all"].abs().clip(lower=1.0)
        if (error / scale).max() > 2e-6:
            raise ValueError(
                f"group wealth: {asset} does not aggregate to supplied total"
            )
    return pd.DataFrame(allocated)


def _known_asset_inflation(
    frame: pd.DataFrame,
    *,
    asset: str,
    group: str,
) -> pd.Series:
    """Return the paper's non-equity valuation factor for one group/asset."""

    return known_asset_inflation(
        frame,
        asset=asset,
        use_top_ten_write_down=group in {"top_1", "next_9"},
    )


def known_asset_inflation(
    frame: pd.DataFrame,
    *,
    asset: str,
    use_top_ten_write_down: bool,
) -> pd.Series:
    """Return a known valuation factor for an arbitrary fine cohort.

    Parameters
    ----------
    frame
        Annual frame containing the supplied housing and debt valuation
        series.
    asset
        One of the balance-sheet categories in :data:`ASSETS`.
    use_top_ten_write_down
        Whether debt in the cohort uses the supplied top-10-percent factor.

    Returns
    -------
    pandas.Series
        Annual valuation factor in decimal units. Liabilities use the negative
        write-down convention required by their negative balance-sheet sign.

    Raises
    ------
    ValueError
        If ``asset`` is not a recognized balance-sheet category.
    """

    if asset not in ASSETS:
        raise ValueError(f"unknown balance-sheet category {asset!r}")
    if asset == "arealest":
        return frame["JST_housing_capgain"]
    if asset not in DEBT_ASSETS:
        return pd.Series(0.0, index=frame.index)
    suffix = "10" if use_top_ten_write_down else "90"
    debt_type = "mdebt" if asset == "lhommort" else "cdebt"
    return -frame[f"ZIP_{debt_type}_wd{suffix}"].fillna(0.0)


def construct_annual_saving(
    group_wealth: pd.DataFrame,
    valuation_inputs: pd.DataFrame,
    private_saving: pd.DataFrame,
) -> pd.DataFrame:
    """Apply the active-saving identity and NIPA residual-equity closure.

    For asset or liability ``j`` and group ``g``, active saving is
    ``W[g,j,t] - (1 + pi[g,j,t]) * W[g,j,t-1]``. The common valuation factor
    for equity-like assets is chosen so reconstructed aggregate saving equals
    NIPA personal plus business saving in every year.
    """

    frame = group_wealth.merge(
        valuation_inputs,
        on="year",
        how="left",
        validate="one_to_one",
    ).merge(
        private_saving,
        on="year",
        how="left",
        validate="one_to_one",
    )
    if frame[["private_saving_millions", "JST_housing_capgain"]].isna().any().any():
        raise ValueError("annual saving: missing required NIPA or housing input")
    frame = frame.sort_values("year").reset_index(drop=True)
    if not (frame["year"].diff().dropna() == 1).all():
        raise ValueError("annual saving: years must be contiguous")

    saving_components: dict[str, pd.Series] = {}
    for group in GROUPS:
        for asset in KNOWN_ASSETS:
            level = frame[f"h{asset}_{group}"]
            inflation = _known_asset_inflation(
                frame,
                asset=asset,
                group=group,
            )
            column = f"saving_{asset}_{group}"
            saving_components[column] = (
                level - (1.0 + inflation) * level.shift(1)
            )

    known_saving = pd.DataFrame(saving_components).sum(axis=1, min_count=1)
    equity_current = sum(
        frame[f"h{asset}_{group}"]
        for asset in RESIDUAL_EQUITY_ASSETS
        for group in GROUPS
    )
    equity_previous = equity_current.shift(1)
    residual_saving = frame["private_saving_millions"] - known_saving
    frame["residual_equity_inflation"] = (
        (equity_current - residual_saving) / equity_previous - 1.0
    )

    for group in GROUPS:
        for asset in RESIDUAL_EQUITY_ASSETS:
            level = frame[f"h{asset}_{group}"]
            saving_components[f"saving_{asset}_{group}"] = level - (
                1.0 + frame["residual_equity_inflation"]
            ) * level.shift(1)
    component_frame = pd.DataFrame(saving_components, index=frame.index)

    output = frame[
        ["year", "NatInc", "private_saving_millions", "residual_equity_inflation"]
    ].copy()
    for group in GROUPS:
        group_columns = [f"saving_{asset}_{group}" for asset in ASSETS]
        output[f"saving_{group}_millions"] = component_frame[group_columns].sum(
            axis=1,
            min_count=1,
        )
        output[f"saving_{group}_to_national_income"] = (
            output[f"saving_{group}_millions"] / output["NatInc"]
        )
    output["saving_bottom_99_millions"] = sum(
        output[f"saving_{group}_millions"]
        for group in ("next_9", "next_40", "bottom_50")
    )
    output["saving_bottom_99_to_national_income"] = (
        output["saving_bottom_99_millions"] / output["NatInc"]
    )
    output["reconstructed_private_saving_millions"] = sum(
        output[f"saving_{group}_millions"] for group in GROUPS
    )
    closure_error = (
        output["reconstructed_private_saving_millions"]
        - output["private_saving_millions"]
    )
    valid = output["residual_equity_inflation"].notna()
    scale = output.loc[valid, "NatInc"].abs().clip(lower=1.0)
    max_relative_error = (closure_error.loc[valid].abs() / scale).max()
    if max_relative_error > 1e-10:
        raise ValueError(
            "annual saving: NIPA private-saving closure failed; "
            f"max error as share of national income={max_relative_error:.3g}"
        )

    output = output.loc[output["year"].between(1963, 2016)].reset_index(drop=True)
    if output["year"].tolist() != list(range(1963, 2017)):
        raise ValueError("annual saving: expected complete 1963-2016 sample")
    return output


def apply_figure5_display(
    annual_saving: pd.DataFrame,
    *,
    window: int = 10,
    base_year: int = 1982,
) -> pd.DataFrame:
    """Apply the July 2025 trailing average and base-year normalization."""

    if window <= 0:
        raise ValueError("Figure 5 display: window must be positive")
    frame = annual_saving.sort_values("year").copy()
    ratio_columns = {
        group: f"saving_{group}_to_national_income"
        for group in (*GROUPS, "bottom_99")
    }
    output = frame[["year"]].copy()
    for group, column in ratio_columns.items():
        moving_column = f"{group}_ma{window}"
        output[moving_column] = frame[column].rolling(
            window=window,
            min_periods=window,
        ).mean()
        base = output.loc[output["year"] == base_year, moving_column]
        if len(base) != 1 or not np.isfinite(base.iloc[0]):
            raise ValueError(
                f"Figure 5 display: unavailable {base_year} moving-average base"
            )
        output[f"{group}_relative_to_{base_year}"] = (
            output[moving_column] - base.iloc[0]
        )
    return output.loc[output[f"top_1_ma{window}"].notna()].reset_index(drop=True)


def build_saving_validation(
    annual_saving: pd.DataFrame,
    benchmark: pd.DataFrame,
    *,
    tolerance: float = 0.003,
) -> pd.DataFrame:
    """Compare fine-share saving with the older coarse Stata series.

    The supplied fine DINA shares are the inputs required for the four-group
    2025 display, but they do not reproduce the kit's older coarse shares
    exactly. The default tolerance is therefore 0.3 percentage points of
    national income; this check diagnoses the input distinction rather than
    asserting bitwise equivalence.
    """

    merged = annual_saving.merge(
        benchmark,
        on="year",
        how="inner",
        validate="one_to_one",
    )
    if len(merged) != len(annual_saving):
        raise ValueError("saving validation: annual merge lost observations")
    mappings = {
        "top_1": "saving_12NI",
        "next_9": "saving_92NI",
        "bottom_90": "saving_902NI",
    }
    records = []
    for group, benchmark_column in mappings.items():
        if group == "bottom_90":
            reconstructed = (
                merged["saving_next_40_to_national_income"]
                + merged["saving_bottom_50_to_national_income"]
            )
        else:
            reconstructed = merged[f"saving_{group}_to_national_income"]
        record = pd.DataFrame(
            {
                "year": merged["year"],
                "group": group,
                "python_ratio": reconstructed,
                "stata_ratio": merged[benchmark_column],
            }
        )
        record["error"] = record["python_ratio"] - record["stata_ratio"]
        records.append(record)
    output = pd.concat(records, ignore_index=True)
    max_error = output["error"].abs().max()
    if max_error > tolerance:
        raise ValueError(
            f"saving validation: Python/Stata error {max_error:.3g} exceeds "
            f"tolerance {tolerance:.3g}"
        )
    return output
