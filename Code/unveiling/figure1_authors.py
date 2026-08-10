"""Figure 1 reconstruction from the authors' February 2021 data snapshot.

The July 2025 paper builds Figure 1 from 34 instrument matrices and 23
intermediary sectors.  Those completed matrices are not part of the older
replication kit.  This module therefore reconstructs the observable numerator
from the earliest feasible supplied inputs:

* the authors' Q4 Financial Accounts panel for household instrument stocks;
* the authors' hand-coded proportional allocation of financial-sector bonds,
  reimplemented here from the same Q4 panel; and
* their licensed CRSP monthly file for a transparent corporate-equity
  extension.

The resulting level relative to national income is directly comparable with
the left axis of Figure 1.  The share uses the closest denominator that can be
formed from the older files and is deliberately named a proxy because the
paper's completed 2025 issuer-holder matrices are unavailable.

This is the project's primary Figure 1 replication evidence.  The independent
newer-public-data robustness pipeline is kept separately in
``unveiling.figure1`` and does not enter any calculation in this module.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

import numpy as np
import pandas as pd


BALANCE_SHEET_COLUMNS: Final[tuple[str, ...]] = (
    "quarter",
    "fl154090005q",  # total household financial assets
    "fl153020005q",  # checkable deposits and currency
    "fl153030005q",  # time and saving deposits
    "fl153034005q",  # money market fund shares
    "lm153061705q",  # agency- and GSE-backed securities
    "lm153064205q",  # mutual fund shares
    "fl153040005q",  # life insurance reserves
    "fl153050005q",  # pension entitlements
    "fl594090055q",  # unfunded pension amount removed by the authors
    "lm153091003q",  # private foreign deposits
    "fl153090005q",  # miscellaneous/residual assets
)

DENOMINATOR_ALLOCATION_COLUMNS: Final[tuple[str, ...]] = (
    "year",
    "a_hh_nfcbnd",
    "a_hh_nfcequity",
    "a_hh_nfcothl",
)

BOND_BENCHMARK_COLUMNS: Final[tuple[str, ...]] = (
    "year",
    "a_hh_absbnd",
    "a_hh_fincbnd",
    "a_hh_mreitbnd",
    "a_hh_pdibnd",
)

BOND_HOLDER_COLUMNS: Final[dict[str, str]] = {
    "hh": "lm153063005q",
    "fgov": "fl313063763q",
    "lgov": "fl213063003q",
    "depinst": "lm763063005q",
    "crun": "lm473063005q",
    "fbank": "lm753063005q",
    "busaf": "lm743063005q",
    "pins": "lm513063095q",
    "lins": "lm543063005q",
    "pens": "lm573063005q",
    "mmf": "fl633063005q",
    "mufu": "lm653063005q",
    "clof": "lm553063003q",
    "etf": "lm563063003q",
    "gse": "fl403063005q",
    "finc": "lm613063003q",
    "ereit": "fl643063083q",
    "mreit": "fl643063073q",
    "brok": "fl663063005q",
    "hold": "lm733063003q",
    "fund": "fl503063005q",
    "row": "lm263063005q",
}

BOND_INPUT_COLUMNS: Final[tuple[str, ...]] = tuple(
    dict.fromkeys(
        (
            "quarter",
            *BOND_HOLDER_COLUMNS.values(),
            "lm343063005q",
            "lm223063045q",
            "lm763063605q",
            "lm473063605q",
            "lm513063605q",
            "lm543063675q",
            "fl403063605q",
            "lm263063603q",
            "lm763063095q",
            "lm473063095q",
            "lm543063095q",
            "lm263063095q",
            "fl673163005q",
            "fl613163005q",
            "fl643163075q",
            "fl763163005q",
            "fl733163003q",
            "fl763194735q",
            "fl513194733q",
            "fl543194733q",
            "fl663194735q",
            "fl263194735q",
        )
    )
)

EQUITY_HOLDER_COLUMNS: Final[tuple[str, ...]] = (
    "lm153064105q",
    "lm103064103q",
    "lm313064105q",
    "lm213064103q",
    "fl713064103q",
    "lm763064105q",
    "fl753064103q",
    "lm513064105q",
    "lm543064105q",
    "lm573064105q",
    "lm343064105q",
    "lm223064145q",
    "lm653064100q",
    "lm553064103q",
    "lm563064100q",
    "lm663064103q",
    "fl503064105q",
    "lm263064105q",
)

COMPONENT_COLUMNS: Final[tuple[str, ...]] = (
    "checkable_deposits_and_currency_millions",
    "time_and_saving_deposits_millions",
    "money_market_fund_shares_millions",
    "agency_gse_securities_millions",
    "mutual_fund_shares_millions",
    "life_insurance_reserves_millions",
    "funded_pension_entitlements_millions",
    "financial_intermediary_bonds_millions",
    "listed_financial_equity_millions",
)


def _require_unique_years(frame: pd.DataFrame, name: str) -> None:
    """Validate the annual key used by every Figure 1 merge."""

    if frame["year"].isna().any():
        raise ValueError(f"{name}: year contains missing values")
    if not frame["year"].is_unique:
        duplicates = frame.loc[frame["year"].duplicated(), "year"].tolist()
        raise ValueError(f"{name}: duplicate years {duplicates[:5]}")


def _load_q4_columns(
    path: Path,
    columns: tuple[str, ...],
    *,
    name: str,
    start_year: int,
    end_year: int,
) -> pd.DataFrame:
    """Load and validate a complete annual Q4 slice of the authors' panel."""

    if not path.is_file():
        raise FileNotFoundError(path)
    frame = pd.read_stata(
        path,
        columns=list(columns),
        convert_categoricals=False,
    )
    if not pd.api.types.is_datetime64_any_dtype(frame["quarter"]):
        raise ValueError(f"{name}: quarter is not a Stata date")

    frame = frame.loc[frame["quarter"].dt.quarter.eq(4)].copy()
    frame["year"] = frame["quarter"].dt.year.astype("int16")
    frame = frame.loc[frame["year"].between(start_year, end_year)]
    frame = frame.drop(columns="quarter").reset_index(drop=True)
    _require_unique_years(frame, name)

    expected_years = set(range(start_year, end_year + 1))
    missing_years = sorted(expected_years - set(frame["year"]))
    if missing_years:
        raise ValueError(f"{name}: missing years {missing_years}")
    if frame.drop(columns="year").isna().any().any():
        missing = frame.drop(columns="year").isna().sum()
        missing = missing[missing.gt(0)].to_dict()
        raise ValueError(f"{name}: missing required values {missing}")
    return frame


def load_author_balance_sheet(
    path: Path,
    *,
    start_year: int = 1963,
    end_year: int = 2016,
) -> pd.DataFrame:
    """Load Q4 household instrument stocks from the authors' wide FOF panel.

    Parameters
    ----------
    path
        Authors' ``LQpanel_2019Q1.dta`` file.
    start_year, end_year
        Inclusive calendar-year range.  The default endpoint is 2016 because
        the authors' prepared national-income series ends in 2016.

    Returns
    -------
    pandas.DataFrame
        One row per year.  Monetary columns are stocks in millions of current
        dollars, as published in the Financial Accounts.

    Raises
    ------
    FileNotFoundError
        If ``path`` is absent.
    ValueError
        If Q4 observations do not form a complete, unique annual panel.
    """

    return _load_q4_columns(
        path,
        BALANCE_SHEET_COLUMNS,
        name="author balance sheet",
        start_year=start_year,
        end_year=end_year,
    )


def load_author_denominator_allocations(
    path: Path,
    *,
    start_year: int = 1963,
    end_year: int = 2016,
) -> pd.DataFrame:
    """Load prepared nonfinancial claims used only in the share proxy.

    These old proportional allocations remove nonfinancial corporate claims
    from the broad household balance-sheet denominator.  They do not enter the
    Figure 1 numerator or its normalization by national income.
    """

    if not path.is_file():
        raise FileNotFoundError(path)
    frame = pd.read_stata(
        path,
        columns=list(DENOMINATOR_ALLOCATION_COLUMNS),
        convert_categoricals=False,
    )
    frame["year"] = frame["year"].astype("int16")
    frame = frame.loc[frame["year"].between(start_year, end_year)].copy()
    _require_unique_years(frame, "author denominator allocations")
    if frame.isna().any().any():
        missing = frame.isna().sum()
        missing = missing[missing.gt(0)].to_dict()
        raise ValueError(
            "author denominator allocations: missing required values "
            f"{missing}"
        )
    return frame.reset_index(drop=True)


def load_author_bond_inputs(
    path: Path,
    *,
    start_year: int = 1963,
    end_year: int = 2016,
) -> pd.DataFrame:
    """Load raw columns needed to allocate intermediary bonds to households.

    The unit is year and every monetary field is a year-end stock in millions
    of current dollars.  The selected fields reproduce the proportional bond
    allocations in ``build_fa_unveiling_data.do`` without reading its final
    ``Yunveilhhd.dta`` output.
    """

    return _load_q4_columns(
        path,
        BOND_INPUT_COLUMNS,
        name="author bond inputs",
        start_year=start_year,
        end_year=end_year,
    )


def load_author_equity_shares(
    path: Path,
    *,
    start_year: int = 1963,
    end_year: int = 2016,
) -> pd.DataFrame:
    """Construct households' share of directly held corporate equity.

    The raw Financial Accounts columns reproduce ``a_hh_equity`` and
    ``a_tot_equity`` at lines 1497--1533 of the old builder.  The share is used
    to allocate the CRSP market capitalization of listed financial issuers.
    """

    columns = ("quarter", *EQUITY_HOLDER_COLUMNS)
    frame = _load_q4_columns(
        path,
        columns,
        name="author equity shares",
        start_year=start_year,
        end_year=end_year,
    )
    output = pd.DataFrame({"year": frame["year"]})
    output["a_hh_equity"] = frame["lm153064105q"]
    output["a_tot_equity"] = frame[list(EQUITY_HOLDER_COLUMNS)].to_numpy(
        dtype=np.float32
    ).sum(axis=1, dtype=np.float32)
    household_share = output["a_hh_equity"] / output["a_tot_equity"]
    if not household_share.between(0, 1).all():
        raise ValueError("author equity shares: invalid household share")
    return output


def load_author_bond_benchmark(
    path: Path,
    *,
    start_year: int = 1963,
    end_year: int = 2016,
) -> pd.DataFrame:
    """Load supplied bond allocations solely as a historical benchmark."""

    if not path.is_file():
        raise FileNotFoundError(path)
    frame = pd.read_stata(
        path,
        columns=list(BOND_BENCHMARK_COLUMNS),
        convert_categoricals=False,
    )
    frame["year"] = frame["year"].astype("int16")
    frame = frame.loc[frame["year"].between(start_year, end_year)].copy()
    _require_unique_years(frame, "author bond benchmark")
    if frame.isna().any().any():
        missing = frame.isna().sum()
        missing = missing[missing.gt(0)].to_dict()
        raise ValueError(f"author bond benchmark: missing values {missing}")
    return frame.reset_index(drop=True)


def construct_author_bond_allocations(
    inputs: pd.DataFrame,
) -> pd.DataFrame:
    """Reimplement the old proportional allocation of intermediary bonds.

    Parameters
    ----------
    inputs
        One row per year from :func:`load_author_bond_inputs`.  Columns are
        year-end Financial Accounts stocks in millions of current dollars.

    Returns
    -------
    pandas.DataFrame
        Household holdings of bonds issued by ABS vehicles, finance companies,
        mortgage REITs, and private depository institutions.  The key is year.

    Notes
    -----
    This is a reconstruction of direct issuer-holder cells, not a seven-round
    unveiling of household debt.  It implements the proportional missing-cell
    rules in the 2021 builder, which are a documented precursor to the revised
    matrix-completion stage of the 2025 paper.
    """

    _require_unique_years(inputs, "author bond inputs")
    frame = inputs.copy()
    for holder, column in BOND_HOLDER_COLUMNS.items():
        frame[f"a_{holder}_bnd"] = frame[column]
    frame["a_govret_bnd"] = frame["lm343063005q"] + frame["lm223063045q"]

    all_holders = (*BOND_HOLDER_COLUMNS.keys(), "govret")
    frame["a_tot_bnd"] = frame[
        [f"a_{holder}_bnd" for holder in all_holders]
    ].sum(axis=1)

    known_abs_sources = {
        "depinst": "lm763063605q",
        "crun": "lm473063605q",
        "pins": "lm513063605q",
        "lins": "lm543063675q",
        "gse": "fl403063605q",
        "row": "lm263063603q",
    }
    other_bond_sources = {
        "depinst": "lm763063095q",
        "crun": "lm473063095q",
        "pins": "lm513063095q",
        "lins": "lm543063095q",
        "row": "lm263063095q",
    }
    for holder, column in known_abs_sources.items():
        frame[f"a_{holder}_absbnd"] = frame[column]
    for holder, column in other_bond_sources.items():
        frame[f"a_{holder}_othbnd"] = frame[column]

    issuer_bonds = frame[
        ["fl673163005q", "fl613163005q", "fl643163075q"]
    ].sum(axis=1)
    frame["d_master_bnd"] = (
        issuer_bonds
        - frame["a_gse_bnd"]
        - frame["a_finc_bnd"]
        - frame["a_mreit_bnd"]
    )
    for prefix, column in {
        "abs": "fl673163005q",
        "finc": "fl613163005q",
        "mreit": "fl643163075q",
    }.items():
        frame[f"d_{prefix}net_bnd"] = (
            frame[column] * frame["d_master_bnd"] / issuer_bonds
        )

    frame["a_totnet_bnd"] = (
        frame["a_tot_bnd"]
        - frame["a_gse_bnd"]
        - frame["a_finc_bnd"]
        - frame["a_mreit_bnd"]
    )
    explicit_abs_holders = ("depinst", "crun", "pins", "lins", "row")
    allocated_holders = (
        "hh",
        "fgov",
        "lgov",
        "fbank",
        "busaf",
        "pens",
        "govret",
        "mmf",
        "mufu",
        "clof",
        "etf",
        "brok",
        "hold",
        "fund",
        "ereit",
    )
    frame["residnet_absbnd"] = frame["d_absnet_bnd"] - frame[
        [f"a_{holder}_absbnd" for holder in explicit_abs_holders]
    ].sum(axis=1)
    frame["residnet_bnd"] = frame["a_totnet_bnd"] - frame[
        [f"a_{holder}_bnd" for holder in explicit_abs_holders]
    ].sum(axis=1)
    for holder in allocated_holders:
        frame[f"a_{holder}_absbnd"] = (
            frame[f"a_{holder}_bnd"]
            / frame["residnet_bnd"]
            * frame["residnet_absbnd"]
        )
    abs_holders = (*explicit_abs_holders, "gse", *allocated_holders)
    frame["a_tot_absbnd"] = frame[
        [f"a_{holder}_absbnd" for holder in abs_holders]
    ].sum(axis=1)
    frame["a_totnet_absbnd"] = (
        frame["a_tot_absbnd"] - frame["a_gse_absbnd"]
    )

    for holder in explicit_abs_holders:
        frame[f"a_{holder}_fincbnd"] = (
            frame[f"a_{holder}_othbnd"]
            / (frame["a_totnet_bnd"] - frame["a_totnet_absbnd"])
            * frame["d_fincnet_bnd"]
        )
    known_finc = frame[
        [f"a_{holder}_fincbnd" for holder in explicit_abs_holders]
    ].sum(axis=1)
    for holder in allocated_holders:
        frame[f"a_{holder}_fincbnd"] = (
            frame[f"a_{holder}_bnd"]
            / frame["residnet_bnd"]
            * (frame["d_fincnet_bnd"] - known_finc)
        )
    finc_holders = (*explicit_abs_holders, *allocated_holders)
    frame["a_tot_fincbnd"] = frame[
        [f"a_{holder}_fincbnd" for holder in finc_holders]
    ].sum(axis=1)
    frame = frame.copy()

    for holder in explicit_abs_holders:
        frame[f"a_{holder}_mreitbnd"] = (
            frame[f"a_{holder}_othbnd"]
            / (
                frame["a_totnet_bnd"]
                - frame["a_totnet_absbnd"]
                - frame["a_tot_fincbnd"]
            )
            * frame["d_mreitnet_bnd"]
        )
    known_mreit = frame[
        [f"a_{holder}_mreitbnd" for holder in explicit_abs_holders]
    ].sum(axis=1)
    for holder in allocated_holders:
        frame[f"a_{holder}_mreitbnd"] = (
            frame[f"a_{holder}_bnd"]
            / frame["residnet_bnd"]
            * (frame["d_mreitnet_bnd"] - known_mreit)
        )
    mreit_holders = (*explicit_abs_holders, *allocated_holders)
    frame["a_tot_mreitbnd"] = frame[
        [f"a_{holder}_mreitbnd" for holder in mreit_holders]
    ].sum(axis=1)
    frame = frame.copy()

    hold_tot = frame[
        [
            "fl763194735q",
            "fl513194733q",
            "fl543194733q",
            "fl663194735q",
            "fl263194735q",
        ]
    ].sum(axis=1)
    frame["d_pdi_bnd_hold"] = (
        frame["fl763163005q"]
        + frame["fl733163003q"] * frame["fl763194735q"] / hold_tot
    ).fillna(0.0)
    pdi_weights = (
        "a_hh_bnd",
        "a_fgov_bnd",
        "a_lgov_bnd",
        "a_pins_othbnd",
        "a_lins_othbnd",
        "a_pens_bnd",
        "a_govret_bnd",
        "a_brok_bnd",
        "a_fund_bnd",
        "a_row_othbnd",
    )
    pdi_denominator = frame[list(pdi_weights)].sum(axis=1)
    frame["a_hh_pdibnd"] = (
        frame["a_hh_bnd"] * frame["d_pdi_bnd_hold"] / pdi_denominator
    )

    output = frame[
        [
            "year",
            "a_hh_absbnd",
            "a_hh_fincbnd",
            "a_hh_mreitbnd",
            "a_hh_pdibnd",
        ]
    ].copy()
    if not np.isfinite(output.drop(columns="year").to_numpy()).all():
        raise ValueError("author bond allocations: non-finite output")
    if (output.drop(columns="year") < 0).any().any():
        raise ValueError("author bond allocations: negative household holdings")

    allocation_checks = (
        ("ABS", "a_totnet_absbnd", "d_absnet_bnd"),
        ("finance company", "a_tot_fincbnd", "d_fincnet_bnd"),
        ("mortgage REIT", "a_tot_mreitbnd", "d_mreitnet_bnd"),
    )
    for issuer, allocated_column, issued_column in allocation_checks:
        residual = frame[allocated_column] - frame[issued_column]
        scale = frame[issued_column].abs().clip(lower=1.0)
        if (residual.abs() / scale > 1e-6).any():
            raise ValueError(
                f"author bond allocations: {issuer} allocation does not close"
            )
    return output.reset_index(drop=True)


def aggregate_crsp_financial_equity(
    path: Path,
    *,
    start_year: int = 1963,
    end_year: int = 2016,
) -> pd.DataFrame:
    """Aggregate December market equity for listed financial intermediaries.

    The filter follows the authors' CRSP support code by excluding securities
    whose two-digit CRSP share code ends in 2 (foreign-incorporated firms).
    Financial intermediaries are classified by SIC 6000--6399 and 6700--6799:
    depositories, non-depository credit, securities firms, insurers, holding
    companies, investment offices, funds, and REITs.  General real-estate
    operators (SIC 6500--6699) are not treated as financial intermediaries.

    CRSP reports price in dollars and shares outstanding in thousands.  Their
    product is divided by 1,000 to obtain millions of current dollars.
    """

    if not path.is_file():
        raise FileNotFoundError(path)
    columns = ["date", "shrcd", "siccd", "prc", "shrout"]
    frame = pd.read_stata(path, columns=columns, convert_categoricals=False)
    if not pd.api.types.is_datetime64_any_dtype(frame["date"]):
        raise ValueError("CRSP: date is not a Stata date")

    frame = frame.loc[
        frame["date"].dt.month.eq(12)
        & frame["date"].dt.year.between(start_year, end_year)
    ].copy()
    share_code = frame["shrcd"].astype("Int64").astype("string").str.zfill(2)
    frame = frame.loc[~share_code.str[-1].eq("2").fillna(False)].copy()
    frame = frame.dropna(subset=["siccd", "prc", "shrout"])

    is_financial = frame["siccd"].between(6000, 6399) | frame[
        "siccd"
    ].between(6700, 6799)
    frame = frame.loc[is_financial]
    frame["year"] = frame["date"].dt.year.astype("int16")
    frame["listed_financial_equity_millions"] = (
        frame["prc"].abs() * frame["shrout"] / 1_000
    )
    annual = (
        frame.groupby("year", as_index=False, sort=True)[
            "listed_financial_equity_millions"
        ]
        .sum()
        .reset_index(drop=True)
    )
    _require_unique_years(annual, "CRSP financial equity")
    expected_years = set(range(start_year, end_year + 1))
    missing_years = sorted(expected_years - set(annual["year"]))
    if missing_years:
        raise ValueError(f"CRSP financial equity: missing years {missing_years}")
    return annual


def load_author_national_income(
    path: Path,
    *,
    start_year: int = 1963,
    end_year: int = 2016,
) -> pd.DataFrame:
    """Load authors-prepared annual national income and convert to millions."""

    if not path.is_file():
        raise FileNotFoundError(path)
    frame = pd.read_stata(
        path,
        columns=["year", "NationalInc"],
        convert_categoricals=False,
    )
    frame["year"] = frame["year"].astype("int16")
    frame = frame.loc[frame["year"].between(start_year, end_year)].copy()
    frame = frame.rename(columns={"NationalInc": "national_income_billions"})
    _require_unique_years(frame, "author national income")
    if frame["national_income_billions"].isna().any():
        raise ValueError("author national income: missing required values")
    frame["national_income_millions"] = (
        frame["national_income_billions"] * 1_000
    )
    return frame.drop(columns="national_income_billions").reset_index(drop=True)


def construct_authors_figure1(
    balance_sheet: pd.DataFrame,
    bond_allocations: pd.DataFrame,
    equity_shares: pd.DataFrame,
    denominator_allocations: pd.DataFrame,
    crsp_equity: pd.DataFrame,
    national_income: pd.DataFrame,
) -> pd.DataFrame:
    """Combine instrument components into the authors-data Figure 1 series.

    The numerator is the explicit sum of the nine columns in
    :data:`COMPONENT_COLUMNS`.  Listed financial equity is allocated to
    households using their share of all directly held corporate equity, the
    same proportionality logic used by the old authors' code for bank equity.

    The share denominator subtracts the old kit's observable nonfinancial,
    rest-of-world, residual, and unfunded-pension items from household total
    financial assets.  It is a proxy for the paper's denominator because the
    completed 2025 issuer-holder matrices are absent.
    """

    merged = balance_sheet.merge(
        bond_allocations, on="year", how="inner", validate="one_to_one"
    )
    merged = merged.merge(
        equity_shares, on="year", how="inner", validate="one_to_one"
    )
    merged = merged.merge(
        denominator_allocations,
        on="year",
        how="inner",
        validate="one_to_one",
    )
    merged = merged.merge(
        crsp_equity, on="year", how="inner", validate="one_to_one"
    )
    merged = merged.merge(
        national_income, on="year", how="inner", validate="one_to_one"
    )
    expected_rows = len(balance_sheet)
    if len(merged) != expected_rows:
        raise ValueError(
            "authors Figure 1: annual merges lost observations "
            f"({expected_rows} expected, {len(merged)} found)"
        )
    _require_unique_years(merged, "authors Figure 1")

    output = pd.DataFrame({"year": merged["year"].astype("int16")})
    output["checkable_deposits_and_currency_millions"] = merged[
        "fl153020005q"
    ]
    output["time_and_saving_deposits_millions"] = merged["fl153030005q"]
    output["money_market_fund_shares_millions"] = merged["fl153034005q"]
    output["agency_gse_securities_millions"] = merged["lm153061705q"]
    output["mutual_fund_shares_millions"] = merged["lm153064205q"]
    output["life_insurance_reserves_millions"] = merged["fl153040005q"]
    output["funded_pension_entitlements_millions"] = (
        merged["fl153050005q"] - merged["fl594090055q"]
    )
    output["financial_intermediary_bonds_millions"] = merged[
        ["a_hh_absbnd", "a_hh_fincbnd", "a_hh_mreitbnd", "a_hh_pdibnd"]
    ].sum(axis=1)

    household_equity_share = merged["a_hh_equity"] / merged["a_tot_equity"]
    if household_equity_share.isna().any() or not household_equity_share.between(
        0, 1
    ).all():
        raise ValueError("authors Figure 1: invalid household equity share")
    output["listed_financial_equity_millions"] = (
        household_equity_share * merged["listed_financial_equity_millions"]
    )

    output["indirect_household_assets_millions"] = output[
        list(COMPONENT_COLUMNS)
    ].sum(axis=1)
    excluded = (
        merged["fl594090055q"]
        + merged["lm153091003q"]
        + merged["fl153090005q"]
        + merged["a_hh_nfcbnd"]
        + merged["a_hh_nfcequity"]
        + merged["a_hh_nfcothl"]
    )
    output["paper_scope_financial_assets_proxy_millions"] = (
        merged["fl154090005q"] - excluded
    )
    output["broad_household_financial_assets_millions"] = (
        merged["fl154090005q"] - merged["fl594090055q"]
    )
    output["national_income_millions"] = merged["national_income_millions"]
    output["indirect_share_proxy"] = (
        output["indirect_household_assets_millions"]
        / output["paper_scope_financial_assets_proxy_millions"]
    )
    output["indirect_share_broad"] = (
        output["indirect_household_assets_millions"]
        / output["broad_household_financial_assets_millions"]
    )
    output["indirect_assets_to_national_income"] = (
        output["indirect_household_assets_millions"]
        / output["national_income_millions"]
    )

    if not np.isfinite(output.drop(columns="year").to_numpy()).all():
        raise ValueError("authors Figure 1: output contains non-finite values")
    if (output["paper_scope_financial_assets_proxy_millions"] <= 0).any():
        raise ValueError("authors Figure 1: non-positive share denominator")
    if not output["indirect_share_proxy"].between(0, 1).all():
        raise ValueError("authors Figure 1: proxy share lies outside [0, 1]")
    return output
