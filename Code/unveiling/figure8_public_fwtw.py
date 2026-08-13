"""Reconstruct 2025 Figure 8 with public FWTW and a full Leontief solve.

This module is deliberately separate from :mod:`unveiling.figure8_authors`.
The older module applies the 2025 net-debt display rule to the February 2021
replication kit's downstream seven-round positions.  This module instead
starts from the Federal Reserve's published instrument-by-issuer-by-holder
levels, expands the household holder into wealth groups with the supplied
DINA shares, and solves the infinite intermediation network.

The reconstruction is mixed-vintage rather than an exact reproduction: the
pinned June 2026 FWTW release has 31 instruments and 25 substantive sectors,
while the paper reports a custom 34-instrument, 27-sector matrix.  The DINA
shares and national income end in 2016 and come from the February 2021 kit.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from .figure1 import read_fwtw
from .wealth_groups import FINE_COHORTS, WEALTH_GROUP_COHORTS


FloatArray = NDArray[np.float64]

GROUPS = ("top_1", "next_9", "next_40", "bottom_50")
DISPLAY_GROUPS = (*GROUPS, "bottom_99")
OTHER_OWNERS = ("federal_government", "state_local_government", "rest_of_world")
OWNERS = (*GROUPS, *OTHER_OWNERS)

HOUSEHOLD_CODE = 15
FEDERAL_GOVERNMENT_CODE = 31
STATE_LOCAL_GOVERNMENT_CODE = 21
REST_OF_WORLD_CODE = 26
TOTAL_SECTOR_CODE = 89
DISCREPANCY_SECTOR_CODE = 90

OWNER_CODE_TO_NAME = {
    FEDERAL_GOVERNMENT_CODE: "federal_government",
    STATE_LOCAL_GOVERNMENT_CODE: "state_local_government",
    REST_OF_WORLD_CODE: "rest_of_world",
}

# Table A1 of the July 2025 paper maps household holdings of each Financial
# Accounts instrument to the DINA asset class used to split the household
# holder.  The current FWTW release aggregates some old lines, so the mapping
# below is the explicit public-taxonomy crosswalk used by this reconstruction.
INSTRUMENT_TO_DINA_CLASS = {
    20500: "taxbond",  # federal funds and repos
    30110: "taxbond",  # monetary gold and SDRs; closest fixed-income class
    30200: "currency",
    30300: "taxbond",
    30305: "taxbond",
    30340: "taxbond",
    30400: "pens",
    30500: "pens",
    30611: "taxbond",
    30617: "taxbond",
    30620: "muni",
    30630: "taxbond",
    30641: "equity",
    30642: "mutual_fund",
    30651: "taxbond",
    30654: "taxbond",
    30655: "taxbond",
    30656: "taxbond",
    30660: "taxbond",
    30680: "taxbond",
    30690: "taxbond",
    30691: "taxbond",
    30700: "taxbond",
    30780: "taxbond",
    30900: "fa",
    30921: "equity",
    30923: "taxbond",
    30930: "fa",
    30940: "fa",
    30949: "bus",
    40100: "taxbond",
}

DINA_CLASSES = tuple(
    sorted(
        {
            class_name
            for class_name in INSTRUMENT_TO_DINA_CLASS.values()
            if class_name != "mutual_fund"
        }
        | {"ownermort", "nonmort"}
    )
)

HOME_MORTGAGE_INSTRUMENT = 30651
NONMORTGAGE_DEBT_INSTRUMENTS = (30660, 30680, 30690, 30900)
HOUSEHOLD_DEBT_INSTRUMENTS = (
    HOME_MORTGAGE_INSTRUMENT,
    *NONMORTGAGE_DEBT_INSTRUMENTS,
)

MUTUAL_FUND_SECTOR_CODE = 65
MUTUAL_FUND_EQUITY_INSTRUMENTS = (30641, 30921, 30949)
MUTUAL_FUND_MUNICIPAL_INSTRUMENTS = (30620,)
MUTUAL_FUND_EXCLUDED_INSTRUMENTS = (30642,)


@dataclass(frozen=True, slots=True)
class AnnualUnveiling:
    """One year's household-debt allocation and network diagnostics.

    Monetary amounts are stocks in millions of current dollars.  ``mode`` is
    either ``"reoriented"`` (negative published positions reverse direction,
    following the Federal Reserve technical note) or ``"clipped"`` (negative
    positions set to zero as a sensitivity).
    """

    year: int
    mode: str
    group_debt_assets: dict[str, float]
    group_debt_liabilities: dict[str, float]
    total_household_debt: float
    diagnostics: dict[str, float | int | str]


def load_distributional_shares(path: Path) -> pd.DataFrame:
    """Load and aggregate fine DINA shares to the four Figure 8 groups.

    Parameters
    ----------
    path
        Authors-kit ``Yszshares_fine.dta`` file.  Each asset-class share is a
        fraction of the aggregate household amount owned or owed by a fine
        wealth cohort.

    Returns
    -------
    pandas.DataFrame
        One row per year and one normalized share column named
        ``{dina_class}_{group}``.  Every class sums to one across groups.
    """

    columns = [
        "year",
        *(
            f"sz{class_name}sh{cohort}"
            for class_name in DINA_CLASSES
            for cohort in FINE_COHORTS
        ),
    ]
    frame = pd.read_stata(path, columns=columns, convert_categoricals=False)
    if pd.api.types.is_datetime64_any_dtype(frame["year"]):
        frame["year"] = frame["year"].dt.year
    years = pd.to_numeric(frame["year"], errors="raise")
    if years.isna().any() or not np.allclose(years, np.rint(years)):
        raise ValueError("DINA shares: year must contain finite integers")
    frame["year"] = np.rint(years).astype(np.int16)
    if frame["year"].duplicated().any():
        raise ValueError("DINA shares: duplicate annual keys")
    numeric = columns[1:]
    frame[numeric] = frame[numeric].astype(np.float64)
    if not np.isfinite(frame[numeric].to_numpy()).all():
        raise ValueError("DINA shares: required shares must be finite")
    if (frame[numeric] < -1e-10).any().any():
        raise ValueError("DINA shares: shares cannot be negative")

    output: dict[str, pd.Series] = {"year": frame["year"]}
    for class_name in DINA_CLASSES:
        fine_columns = [
            f"sz{class_name}sh{cohort}" for cohort in FINE_COHORTS
        ]
        fine_sum = frame[fine_columns].sum(axis=1)
        if (fine_sum - 1.0).abs().max() > 2e-6:
            raise ValueError(
                f"DINA shares: {class_name} fine shares do not sum to one"
            )
        grouped = []
        for group in GROUPS:
            group_columns = [
                f"sz{class_name}sh{cohort}"
                for cohort in WEALTH_GROUP_COHORTS[group]
            ]
            grouped.append(frame[group_columns].sum(axis=1))
        group_frame = pd.concat(grouped, axis=1)
        group_frame.columns = GROUPS
        group_frame = group_frame.div(group_frame.sum(axis=1), axis=0)
        for group in GROUPS:
            output[f"{class_name}_{group}"] = group_frame[group]
    result = pd.DataFrame(output).sort_values("year").reset_index(drop=True)
    return result.loc[result["year"].between(1963, 2016)].reset_index(drop=True)


def load_authors_national_income(path: Path) -> pd.DataFrame:
    """Load authors-kit national income in millions of current dollars."""

    frame = pd.read_stata(
        path,
        columns=["year", "NatInc"],
        convert_categoricals=False,
    )
    years = pd.to_numeric(frame["year"], errors="raise")
    values = pd.to_numeric(frame["NatInc"], errors="raise")
    output = pd.DataFrame(
        {
            "year": np.rint(years).astype(np.int16),
            "national_income_millions": values.astype(np.float64),
        }
    )
    output = output.loc[output["year"].between(1963, 2016)].copy()
    if output["year"].duplicated().any():
        raise ValueError("national income: duplicate annual keys")
    if not np.isfinite(output["national_income_millions"]).all():
        raise ValueError("national income: values must be finite")
    if (output["national_income_millions"] <= 0).any():
        raise ValueError("national income: values must be positive")
    return output.sort_values("year").reset_index(drop=True)


def construct_public_fwtw_figure8(
    fwtw: pd.DataFrame,
    distributional_shares: pd.DataFrame,
    national_income: pd.DataFrame,
    *,
    start_year: int = 1963,
    end_year: int = 2016,
    base_year: int = 1982,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Apply the augmented full-Leontief Figure 8 procedure.

    The primary result reorients negative published positions before building
    the matrix, following the Federal Reserve's interpretation that the
    economic ``from`` and ``to`` are reversed.  The clipped result is a
    sensitivity that sets those positions to zero.  Both exclude published
    total and discrepancy pseudo-sectors and use Q4 stocks.

    Returns
    -------
    result, sensitivity, diagnostics : tuple of pandas.DataFrame
        ``result`` is the reoriented public-FWTW reconstruction;
        ``sensitivity`` is its zero-clipped counterpart; ``diagnostics``
        contains one row per year and mode with matrix and accounting checks.
    """

    years = list(range(start_year, end_year + 1))
    if start_year > end_year or base_year not in years:
        raise ValueError("Figure 8 sample must contain a valid base year")
    shares = distributional_shares.loc[
        distributional_shares["year"].between(start_year, end_year)
    ].copy()
    income = national_income.loc[
        national_income["year"].between(start_year, end_year)
    ].copy()
    for label, frame in (("DINA shares", shares), ("national income", income)):
        if frame["year"].tolist() != years:
            missing = sorted(set(years) - set(frame["year"]))
            raise ValueError(f"{label}: incomplete annual sample; missing={missing}")

    year_end = fwtw.loc[fwtw["Date"].str.endswith("Q4")].copy()
    year_end["year"] = year_end["Date"].str[:4].astype(int)
    year_end = year_end.loc[year_end["year"].between(start_year, end_year)]
    if sorted(year_end["year"].unique().tolist()) != years:
        raise ValueError("FWTW: incomplete Q4 annual sample")
    instrument_codes = set(year_end["Instrument Code"].unique())
    unknown_instruments = sorted(instrument_codes - set(INSTRUMENT_TO_DINA_CLASS))
    if unknown_instruments:
        raise ValueError(f"FWTW: unmapped instruments {unknown_instruments}")

    share_lookup = shares.set_index("year")
    records: dict[str, list[AnnualUnveiling]] = {
        "reoriented": [],
        "clipped": [],
    }
    for year in years:
        annual = year_end.loc[year_end["year"] == year].copy()
        share_row = share_lookup.loc[year]
        mutual_fund_weights = _mutual_fund_asset_weights(annual)
        for mode in records:
            prepared, negative_diagnostics = _prepare_negative_positions(
                annual,
                mode=mode,
            )
            expanded = _expand_household_holder(
                prepared,
                share_row,
                mutual_fund_weights,
            )
            records[mode].append(
                _unveil_household_debt(
                    prepared,
                    expanded,
                    share_row,
                    year=year,
                    mode=mode,
                    mutual_fund_weights=mutual_fund_weights,
                    negative_diagnostics=negative_diagnostics,
                )
            )

    primary = _annual_results_to_frame(records["reoriented"])
    clipped = _annual_results_to_frame(records["clipped"])
    result = _scale_and_normalize(primary, income, base_year=base_year)
    sensitivity = _scale_and_normalize(clipped, income, base_year=base_year)
    diagnostics = pd.DataFrame(
        [item.diagnostics for mode in records.values() for item in mode]
    ).sort_values(["year", "mode"]).reset_index(drop=True)
    return result, sensitivity, diagnostics


def _prepare_negative_positions(
    annual: pd.DataFrame,
    *,
    mode: str,
) -> tuple[pd.DataFrame, dict[str, float | int]]:
    """Apply the declared treatment of negative public FWTW positions.

    The Federal Reserve explains that a negative level can generally be read
    as the economic ``from`` and ``to`` being reversed.  The primary mode
    implements that interpretation at the instrument level before the
    household column is allocated to wealth groups.  The sensitivity simply
    removes negative positions.
    """

    if mode not in {"reoriented", "clipped"}:
        raise ValueError(f"unknown FWTW negative-cell mode {mode!r}")
    substantive = annual.loc[
        ~annual["Issuer Code"].isin([TOTAL_SECTOR_CODE, DISCREPANCY_SECTOR_CODE])
        & ~annual["Holder Code"].isin(
            [TOTAL_SECTOR_CODE, DISCREPANCY_SECTOR_CODE]
        )
    ].copy()
    negative = substantive.loc[substantive["Level"] < 0.0].copy()
    positive = substantive.loc[substantive["Level"] >= 0.0].copy()
    diagnostics: dict[str, float | int] = {
        "negative_input_cells": int(len(negative)),
        "negative_input_abs_millions": float(-negative["Level"].sum()),
        "negative_input_abs_share": float(
            -negative["Level"].sum() / substantive["Level"].abs().sum()
        ),
    }
    if mode == "reoriented" and not negative.empty:
        reversed_positions = negative.copy()
        reversed_positions[["Issuer Code", "Holder Code"]] = negative[
            ["Holder Code", "Issuer Code"]
        ].to_numpy()
        reversed_positions[["Issuer Name", "Holder Name"]] = negative[
            ["Holder Name", "Issuer Name"]
        ].to_numpy()
        reversed_positions["Level"] = -negative["Level"]
        positive = pd.concat([positive, reversed_positions], ignore_index=True)
    key = [
        "Instrument Name",
        "Instrument Code",
        "Holder Name",
        "Holder Code",
        "Issuer Name",
        "Issuer Code",
        "Date",
        "year",
    ]
    prepared = positive.groupby(key, as_index=False, observed=True)["Level"].sum()
    if (prepared["Level"] < -1e-10).any():
        raise ValueError("negative-position preparation did not remove negatives")
    return prepared, diagnostics


def _distribution_vector(
    share_row: pd.Series,
    class_name: str,
    mutual_fund_weights: dict[str, float],
) -> FloatArray:
    """Return four group shares for one public FWTW instrument class."""

    if class_name == "mutual_fund":
        vector = sum(
            mutual_fund_weights[component]
            * np.array(
                [share_row[f"{component}_{group}"] for group in GROUPS],
                dtype=float,
            )
            for component in ("equity", "taxbond", "muni")
        )
    else:
        vector = np.array(
            [share_row[f"{class_name}_{group}"] for group in GROUPS],
            dtype=float,
        )
    if not np.isfinite(vector).all() or (vector < -1e-10).any():
        raise ValueError(f"invalid DINA distribution for class {class_name}")
    vector = vector / vector.sum()
    return vector


def _mutual_fund_asset_weights(annual: pd.DataFrame) -> dict[str, float]:
    """Estimate mutual-fund equity, taxable-bond, and muni portfolio shares.

    This mirrors Table A1's three-way decomposition of household mutual-fund
    shares, but estimates the weights from the same public FWTW vintage.  The
    mutual-fund sector's direct asset positions are summed by instrument;
    negative positions are set to zero only for this portfolio-composition
    calculation, because the weights must form a non-negative partition.
    """

    assets = annual.loc[
        (annual["Holder Code"] == MUTUAL_FUND_SECTOR_CODE)
        & ~annual["Issuer Code"].isin(
            [TOTAL_SECTOR_CODE, DISCREPANCY_SECTOR_CODE]
        )
        & ~annual["Instrument Code"].isin(MUTUAL_FUND_EXCLUDED_INSTRUMENTS)
    ].copy()
    by_instrument = assets.groupby("Instrument Code")["Level"].sum().clip(lower=0.0)
    equity = float(
        by_instrument.reindex(
            MUTUAL_FUND_EQUITY_INSTRUMENTS,
            fill_value=0,
        ).sum()
    )
    muni = float(
        by_instrument.reindex(MUTUAL_FUND_MUNICIPAL_INSTRUMENTS, fill_value=0).sum()
    )
    bond = float(
        by_instrument.drop(
            list(MUTUAL_FUND_EQUITY_INSTRUMENTS)
            + list(MUTUAL_FUND_MUNICIPAL_INSTRUMENTS),
            errors="ignore",
        ).sum()
    )
    total = equity + bond + muni
    if total <= 0:
        raise ValueError("mutual-fund portfolio has no positive public FWTW assets")
    return {"equity": equity / total, "taxbond": bond / total, "muni": muni / total}


def _expand_household_holder(
    annual: pd.DataFrame,
    share_row: pd.Series,
    mutual_fund_weights: dict[str, float],
) -> pd.DataFrame:
    """Replace the aggregate household holder with four wealth-group holders."""

    substantive = annual.loc[
        ~annual["Issuer Code"].isin([TOTAL_SECTOR_CODE, DISCREPANCY_SECTOR_CODE])
        & ~annual["Holder Code"].isin(
            [TOTAL_SECTOR_CODE, DISCREPANCY_SECTOR_CODE]
        ),
        ["Instrument Code", "Issuer Code", "Holder Code", "Level"],
    ].copy()
    nonhousehold = substantive.loc[substantive["Holder Code"] != HOUSEHOLD_CODE].copy()
    nonhousehold["destination"] = nonhousehold["Holder Code"].map(
        OWNER_CODE_TO_NAME
    )
    nonhousehold["destination"] = nonhousehold["destination"].where(
        nonhousehold["destination"].notna(),
        nonhousehold["Holder Code"].map(lambda code: f"sector_{int(code)}"),
    )

    household = substantive.loc[substantive["Holder Code"] == HOUSEHOLD_CODE]
    expanded_records: list[pd.DataFrame] = [nonhousehold]
    for instrument_code, rows in household.groupby("Instrument Code", sort=False):
        class_name = INSTRUMENT_TO_DINA_CLASS[int(instrument_code)]
        vector = _distribution_vector(share_row, class_name, mutual_fund_weights)
        for group, group_share in zip(GROUPS, vector, strict=True):
            allocated = rows.copy()
            allocated["Level"] = allocated["Level"] * group_share
            allocated["destination"] = group
            expanded_records.append(allocated)
    expanded = pd.concat(expanded_records, ignore_index=True)
    return expanded[["Instrument Code", "Issuer Code", "destination", "Level"]]


def _unveil_household_debt(
    annual: pd.DataFrame,
    expanded: pd.DataFrame,
    share_row: pd.Series,
    *,
    year: int,
    mode: str,
    mutual_fund_weights: dict[str, float],
    negative_diagnostics: dict[str, float | int],
) -> AnnualUnveiling:
    """Build one augmented direct matrix and allocate household debt."""

    if mode not in {"reoriented", "clipped"}:
        raise ValueError(f"unknown FWTW negative-cell mode {mode!r}")
    sector_codes = sorted(
        set(
            annual.loc[
                ~annual["Issuer Code"].isin(
                    [TOTAL_SECTOR_CODE, DISCREPANCY_SECTOR_CODE]
                ),
                "Issuer Code",
            ]
        )
        | set(
            annual.loc[
                ~annual["Holder Code"].isin(
                    [TOTAL_SECTOR_CODE, DISCREPANCY_SECTOR_CODE]
                ),
                "Holder Code",
            ]
        )
    )
    economic_owner_codes = {
        HOUSEHOLD_CODE,
        *OWNER_CODE_TO_NAME,
    }
    intermediary_candidates = [
        code for code in sector_codes if code not in economic_owner_codes
    ]
    aggregate = expanded.groupby(
        ["Issuer Code", "destination"], as_index=False
    )["Level"].sum()

    row_activity = aggregate.groupby("Issuer Code")["Level"].apply(
        lambda values: float(values.abs().sum())
    )
    column_activity = aggregate.groupby("destination")["Level"].apply(
        lambda values: float(values.abs().sum())
    )
    active_intermediaries = [
        code
        for code in intermediary_candidates
        if row_activity.get(code, 0.0) > 1e-9
    ]
    holder_only = [
        code
        for code in intermediary_candidates
        if row_activity.get(code, 0.0) <= 1e-9
        and column_activity.get(f"sector_{code}", 0.0) > 1e-9
    ]
    if holder_only:
        raise ValueError(
            f"{year}: intermediary holders have no issued liabilities {holder_only}"
        )
    inactive_destinations = {
        f"sector_{code}"
        for code in intermediary_candidates
        if code not in active_intermediaries
    }
    excluded_activity = aggregate.loc[
        aggregate["destination"].isin(inactive_destinations), "Level"
    ].abs().sum()
    if excluded_activity > 1e-6:
        raise ValueError(f"{year}: inactive intermediary columns contain activity")

    destinations = [*OWNERS, *(f"sector_{code}" for code in active_intermediaries)]
    matrix_frame = (
        aggregate.loc[aggregate["Issuer Code"].isin(active_intermediaries)]
        .pivot(index="Issuer Code", columns="destination", values="Level")
        .reindex(index=active_intermediaries, columns=destinations, fill_value=0.0)
        .fillna(0.0)
    )
    levels = matrix_frame.to_numpy(dtype=float)
    if (levels < -1e-10).any():
        raise ValueError(f"{year}: prepared direct matrix contains negatives")
    row_totals = levels.sum(axis=1)
    if (row_totals <= 0.0).any():
        bad = [
            code
            for code, value in zip(active_intermediaries, row_totals, strict=True)
            if value <= 0.0
        ]
        raise ValueError(f"{year}: nonpositive intermediary liabilities {bad}")
    direct = levels / row_totals[:, None]
    owner_block = direct[:, : len(OWNERS)]
    cross_block = direct[:, len(OWNERS) :]
    spectral_radius = float(np.max(np.abs(np.linalg.eigvals(cross_block))))
    if spectral_radius >= 1.0 - 1e-10:
        raise ValueError(f"{year}: intermediary chains do not converge")
    omega = np.linalg.solve(
        np.eye(len(active_intermediaries)) - cross_block,
        owner_block,
    )
    omega_row_error = float(np.max(np.abs(omega.sum(axis=1) - 1.0)))
    if omega_row_error > 1e-9:
        raise ValueError(f"{year}: unveiled ownership does not sum to one")

    debt = expanded.loc[
        (expanded["Issuer Code"] == HOUSEHOLD_CODE)
        & expanded["Instrument Code"].isin(HOUSEHOLD_DEBT_INSTRUMENTS)
    ].groupby("destination")["Level"].sum()
    debt_vector = debt.reindex(destinations, fill_value=0.0).to_numpy(dtype=float)
    if (debt_vector < -1e-10).any():
        raise ValueError(f"{year}: prepared household-debt positions are negative")
    total_debt = float(debt_vector.sum())
    if total_debt <= 0:
        raise ValueError(f"{year}: household debt must be positive")
    direct_debt_shares = debt_vector / total_debt
    final_debt_shares = (
        direct_debt_shares[len(OWNERS) :] @ omega
        + direct_debt_shares[: len(OWNERS)]
    )
    primary_sum_error = float(abs(final_debt_shares.sum() - 1.0))
    if primary_sum_error > 1e-9:
        raise ValueError(f"{year}: primary household-debt allocation failed")

    instrument_totals = (
        annual.loc[
            (annual["Issuer Code"] == HOUSEHOLD_CODE)
            & annual["Instrument Code"].isin(HOUSEHOLD_DEBT_INSTRUMENTS)
            & ~annual["Holder Code"].isin(
                [TOTAL_SECTOR_CODE, DISCREPANCY_SECTOR_CODE]
            )
        ]
        .groupby("Instrument Code")["Level"]
        .sum()
    )
    mortgage_total = float(instrument_totals.get(HOME_MORTGAGE_INSTRUMENT, 0.0))
    nonmortgage_total = float(
        instrument_totals.reindex(NONMORTGAGE_DEBT_INSTRUMENTS, fill_value=0.0).sum()
    )
    if not np.isclose(total_debt, mortgage_total + nonmortgage_total, atol=1e-5):
        raise ValueError(f"{year}: household debt instrument totals do not close")

    group_assets = {
        group: float(total_debt * final_debt_shares[index])
        for index, group in enumerate(GROUPS)
    }
    group_liabilities = {
        group: float(
            mortgage_total * share_row[f"ownermort_{group}"]
            + nonmortgage_total * share_row[f"nonmort_{group}"]
        )
        for group in GROUPS
    }
    liability_sum_error = abs(sum(group_liabilities.values()) - total_debt)
    if liability_sum_error / total_debt > 2e-6:
        raise ValueError(f"{year}: group household liabilities do not close")

    diagnostics: dict[str, float | int | str] = {
        "year": year,
        "mode": mode,
        "published_instruments": int(annual["Instrument Code"].nunique()),
        "substantive_sectors": int(len(sector_codes)),
        "active_intermediaries": int(len(active_intermediaries)),
        "inactive_intermediaries": int(
            len(intermediary_candidates) - len(active_intermediaries)
        ),
        **negative_diagnostics,
        "spectral_radius": spectral_radius,
        "direct_row_sum_max_error": float(
            np.max(np.abs(direct.sum(axis=1) - 1.0))
        ),
        "omega_row_sum_max_error": omega_row_error,
        "omega_minimum_share": float(omega.min()),
        "omega_negative_abs_share": float(
            -omega[omega < 0.0].sum() / np.abs(omega).sum()
        ),
        "primary_asset_sum_error": primary_sum_error,
        "primary_minimum_share": float(final_debt_shares.min()),
        "liability_sum_error_millions": float(liability_sum_error),
        "mutual_fund_equity_share": mutual_fund_weights["equity"],
        "mutual_fund_taxbond_share": mutual_fund_weights["taxbond"],
        "mutual_fund_muni_share": mutual_fund_weights["muni"],
        "household_debt_millions": total_debt,
    }
    return AnnualUnveiling(
        year=year,
        mode=mode,
        group_debt_assets=group_assets,
        group_debt_liabilities=group_liabilities,
        total_household_debt=total_debt,
        diagnostics=diagnostics,
    )


def _annual_results_to_frame(results: list[AnnualUnveiling]) -> pd.DataFrame:
    """Convert annual network results to the stable analysis schema."""

    rows: list[dict[str, float | int]] = []
    for item in results:
        row: dict[str, float | int] = {
            "year": item.year,
            "household_debt_millions": item.total_household_debt,
        }
        for group in GROUPS:
            assets = item.group_debt_assets[group]
            liabilities = item.group_debt_liabilities[group]
            row[f"debt_assets_{group}_millions"] = assets
            row[f"debt_liabilities_{group}_millions"] = liabilities
            row[f"net_debt_{group}_millions"] = assets - liabilities
        for measure in ("debt_assets", "debt_liabilities", "net_debt"):
            row[f"{measure}_bottom_99_millions"] = sum(
                float(row[f"{measure}_{group}_millions"])
                for group in ("next_9", "next_40", "bottom_50")
            )
        rows.append(row)
    return pd.DataFrame(rows)


def _scale_and_normalize(
    frame: pd.DataFrame,
    national_income: pd.DataFrame,
    *,
    base_year: int,
) -> pd.DataFrame:
    """Divide net-debt stocks by national income and subtract 1982 levels."""

    output = frame.merge(
        national_income,
        on="year",
        how="left",
        validate="one_to_one",
        indicator=True,
    )
    if not output["_merge"].eq("both").all():
        raise ValueError("Figure 8: national-income merge left unmatched years")
    output = output.drop(columns="_merge")
    for group in DISPLAY_GROUPS:
        ratio = (
            output[f"net_debt_{group}_millions"]
            / output["national_income_millions"]
        )
        base = ratio.loc[output["year"] == base_year]
        if len(base) != 1:
            raise ValueError(f"Figure 8: missing unique {base_year} base")
        output[f"net_debt_{group}_to_national_income"] = ratio
        output[f"net_debt_{group}_relative_to_{base_year}"] = ratio - base.iloc[0]
    return output.sort_values("year").reset_index(drop=True)


__all__ = [
    "DISPLAY_GROUPS",
    "DINA_CLASSES",
    "GROUPS",
    "HOUSEHOLD_DEBT_INSTRUMENTS",
    "INSTRUMENT_TO_DINA_CLASS",
    "construct_public_fwtw_figure8",
    "load_authors_national_income",
    "load_distributional_shares",
    "read_fwtw",
]
