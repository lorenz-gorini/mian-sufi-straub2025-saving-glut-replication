"""Figure 1 reconstruction from the authors' February 2021 data snapshot.

The July 2025 paper builds Figure 1 from 34 instrument matrices and 23
intermediary sectors.  Those completed matrices are not part of the older
replication kit.  This module therefore reconstructs the observable numerator
from the earliest feasible supplied inputs:

* the authors' Q4 Financial Accounts panel for household instrument stocks;
* their prepared issuer allocation for financial-sector bonds; and
* their licensed CRSP monthly file for a transparent corporate-equity
  extension.

The resulting level relative to national income is directly comparable with
the left axis of Figure 1.  The share uses the closest denominator that can be
formed from the older files and is deliberately named a proxy because the
paper's completed 2025 issuer-holder matrices are unavailable.
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

DERIVED_ALLOCATION_COLUMNS: Final[tuple[str, ...]] = (
    "year",
    "a_hh_absbnd",
    "a_hh_fincbnd",
    "a_hh_mreitbnd",
    "a_hh_pdibnd",
    "a_hh_equity",
    "a_tot_equity",
    "a_hh_nfcbnd",
    "a_hh_nfcequity",
    "a_hh_nfcothl",
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

    if not path.is_file():
        raise FileNotFoundError(path)
    frame = pd.read_stata(
        path,
        columns=list(BALANCE_SHEET_COLUMNS),
        convert_categoricals=False,
    )
    if not pd.api.types.is_datetime64_any_dtype(frame["quarter"]):
        raise ValueError("author balance sheet: quarter is not a Stata date")

    frame = frame.loc[frame["quarter"].dt.quarter.eq(4)].copy()
    frame["year"] = frame["quarter"].dt.year.astype("int16")
    frame = frame.loc[frame["year"].between(start_year, end_year)]
    frame = frame.drop(columns="quarter").reset_index(drop=True)
    _require_unique_years(frame, "author balance sheet")

    expected_years = set(range(start_year, end_year + 1))
    missing_years = sorted(expected_years - set(frame["year"]))
    if missing_years:
        raise ValueError(f"author balance sheet: missing years {missing_years}")
    if frame.drop(columns="year").isna().any().any():
        missing = frame.drop(columns="year").isna().sum()
        missing = missing[missing.gt(0)].to_dict()
        raise ValueError(f"author balance sheet: missing required values {missing}")
    return frame


def load_author_allocations(
    path: Path,
    *,
    start_year: int = 1963,
    end_year: int = 2016,
) -> pd.DataFrame:
    """Load the old authors' prepared bond and nonfinancial allocations.

    The selected columns are intermediate outputs of
    ``build_fa_unveiling_data.do``.  Reading them avoids translating the
    entire seven-round debt procedure while retaining the economically
    relevant instrument components for our explicit Figure 1 sum.
    """

    if not path.is_file():
        raise FileNotFoundError(path)
    frame = pd.read_stata(
        path,
        columns=list(DERIVED_ALLOCATION_COLUMNS),
        convert_categoricals=False,
    )
    frame["year"] = frame["year"].astype("int16")
    frame = frame.loc[frame["year"].between(start_year, end_year)].copy()
    _require_unique_years(frame, "author allocations")
    if frame.isna().any().any():
        missing = frame.isna().sum()
        missing = missing[missing.gt(0)].to_dict()
        raise ValueError(f"author allocations: missing required values {missing}")
    return frame.reset_index(drop=True)


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
    allocations: pd.DataFrame,
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
        allocations, on="year", how="inner", validate="one_to_one"
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
