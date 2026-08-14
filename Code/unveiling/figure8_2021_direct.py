"""Apply the full Leontief operator to the 2021 kit's direct-cell vintage.

This module is the third Figure 8 route.  It deliberately sits between the
older seven-round proxy in :mod:`unveiling.figure8_authors` and the newer
public-FWTW reconstruction in :mod:`unveiling.figure8_public_fwtw`:

* data vintage and bilateral-cell completion come from the February 2021 kit;
* no round-one through round-seven household-debt output is read; and
* the completed direct rows are unveiled with ``(I - Q)^{-1} B``.

The old Stata program did not save a rectangular instrument-by-sector cube.
It saved the completed cells used by its seven sequential intermediary
blocks.  We therefore reconstruct eight economically named intermediary rows
from those cells.  Sectors that the old program never unveiled (brokers,
holding/funding companies, nonprofits, and residual balance-sheet items) are
kept in an explicit ``unassigned`` ultimate-owner column.  Negative direct
cells are clipped before each component is rescaled to its authors-kit
liability margin; the amount clipped is reported, never hidden.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
import re

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from .figure8_public_fwtw import (
    DISPLAY_GROUPS,
    GROUPS,
    load_authors_national_income,
    load_distributional_shares,
)


FloatArray = NDArray[np.float64]

OTHER_OWNERS = (
    "federal_government",
    "state_local_government",
    "rest_of_world",
    "unassigned",
)
OWNERS = (*GROUPS, *OTHER_OWNERS)
INTERMEDIARIES = (
    "mortgage_complex",
    "monetary_authority",
    "money_market_funds",
    "mutual_funds",
    "private_depositories",
    "nonfinancial_corporate",
    "nonfinancial_noncorporate",
    "property_casualty_insurance",
)
DEBT_CATEGORIES = ("home_mortgage", "consumer_credit")

_PROHIBITED_SOURCE = re.compile(
    r"(?:_hhd[1-7]$|^a_hh_hhd$|_hhdSZ$|^a_(?:gov|row|oth)_hhd$)"
)

_GSE_SECURITY_HOLDERS = (
    "hh", "nfc", "fgov", "lgov", "depinst", "fbank", "busaf", "crun",
    "lins", "pens", "govret", "mone", "pins", "mmf", "mufu", "brok",
    "hold", "row",
)
_INTERMEDIARY_BOND_HOLDERS = (
    "depinst", "crun", "pins", "lins", "row", "hh", "fgov", "lgov",
    "fbank", "busaf", "pens", "govret", "mmf", "mufu", "clof", "etf",
    "brok", "hold", "fund", "ereit",
)
_COMMERCIAL_PAPER_HOLDERS = (
    "nfc", "lgov", "mone", "depinst", "fbank", "crun", "pins", "lins",
    "pens", "govret", "mmf", "mufu", "brok", "fund", "row",
)
_MMF_HOLDERS = (
    "hh", "nfc", "nfnc", "lgov", "pins", "lins", "pens", "govret",
    "fund", "row",
)
_MUTUAL_FUND_HOLDERS = (
    "hh", "nfc", "lgov", "depinst", "crun", "pins", "lins", "pens",
    "govret", "row",
)
_TIME_DEPOSIT_HOLDERS = (
    "hh", "nfc", "nfnc", "finc", "fgov", "lgov", "pens", "govret",
    "mmf", "gse", "hold", "row",
)
_CHECK_DEPOSIT_HOLDERS = (
    "hh", "nfc", "nfnc", "fgov", "lgov", "pins", "lins", "pens",
    "govret", "brok", "finc", "mmf", "gse", "reit", "row",
)
_PDI_BOND_HOLDERS = (
    "hh", "fgov", "lgov", "pens", "govret", "brok", "fund", "pins",
    "lins", "row",
)
_PDI_CP_HOLDERS = (
    "nfc", "lgov", "mone", "pins", "lins", "pens", "govret", "brok",
    "fund", "row",
)
_PDI_EQUITY_HOLDERS = (
    "hh", "fgov", "lgov", "mone", "pins", "lins", "pens", "govret",
    "nfc", "mufu", "clof", "etf", "brok", "fund", "row",
)
_NFC_CP_HOLDERS = (
    "lgov", "mone", "depinst", "fbank", "crun", "pins", "lins", "pens",
    "govret", "mmf", "mufu", "gse", "brok", "fund", "row",
)
_NFC_BOND_HOLDERS = (
    "hh", "fgov", "lgov", "pdi", "pins", "lins", "pens", "govret",
    "mmf", "mufu", "clof", "etf", "gse", "finc", "ereit", "mreit",
    "brok", "hold", "fund", "row",
)
_NFC_EQUITY_HOLDERS = (
    "hh", "fgov", "lgov", "mone", "pdi", "pins", "lins", "pens",
    "govret", "mufu", "clof", "etf", "brok", "fund", "row",
)
_NFC_OTHER_LOAN_HOLDERS = (
    "hh", "lins", "mufu", "abs", "brok", "fund", "fgov", "fdi", "hold",
    "gse", "finc",
)
_HOUSEHOLD_MORTGAGE_HOLDERS = (
    "hh", "nfc", "nfnc", "fgov", "lgov", "depinst", "fbank", "busaf",
    "crun", "lins", "pens", "govret", "gse", "agpool", "abs", "finc",
    "ereit", "mreit",
)
_HOUSEHOLD_CONSUMER_CREDIT_HOLDERS = (
    "npo", "nfc", "nfnc", "fgov", "depinst", "crun", "gse", "abs", "finc",
)

_MONETARY_CURRENCY_HOLDERS = (
    "hh", "nfc", "nfnc", "lgov", "pins", "lins", "pens", "govret",
    "mmf", "gse", "finc", "reit", "brok",
)
_MONETARY_REPO_HOLDERS = (
    "nfc", "lgov", "gse", "pins", "lins", "pens", "govret", "mmf",
    "mufu", "brok", "hold", "fund", "row",
)

_MUTUAL_FUND_RAW_COLUMNS = (
    "lm654091603q",
    "lm654092603q",
    "lm654091303q",
    "lm654091203q",
    "lm653062003q",
    "lm654090000q",
    "lm654091403q",
    "lm653064100q",
)

_STRUCTURAL_ZERO_COLUMNS = (
    "a_depinst_netsrps",
    "a_fbank_netsrps",
    "a_crun_srps",
)


def _cell_columns(prefix: str, holders: Sequence[str]) -> tuple[str, ...]:
    return tuple(f"a_{holder}_{prefix}" for holder in holders)


DIRECT_SOURCE_COLUMNS = (
    "year",
    "d_hh_hmort",
    "d_hh_ccred",
    "a_hhd_tot",
    *_cell_columns("hmort", _HOUSEHOLD_MORTGAGE_HOLDERS),
    *_cell_columns("ccred", _HOUSEHOLD_CONSUMER_CREDIT_HOLDERS),
    "d_master_gsesec",
    *_cell_columns("gsegsesec", _GSE_SECURITY_HOLDERS),
    "d_absnet_bnd",
    "d_fincnet_bnd",
    "d_mreitnet_bnd",
    *_cell_columns("absbnd", _INTERMEDIARY_BOND_HOLDERS),
    *_cell_columns("fincbnd", _INTERMEDIARY_BOND_HOLDERS),
    *_cell_columns("mreitbnd", _INTERMEDIARY_BOND_HOLDERS),
    "d_master_cpap",
    "d_mreit_resid",
    *_cell_columns("cpap", _COMMERCIAL_PAPER_HOLDERS),
    "d_mone_dpires",
    "d_mone_dpicsh",
    "d_mone_dforiegn",
    "d_mone_curnb",
    "d_mone_srps",
    "d_mone_rsrps",
    "d_mone_resid",
    *_cell_columns("chkcur", _MONETARY_CURRENCY_HOLDERS),
    "a_row_cur",
    "a_depinst_netsrps",
    "a_fbank_netsrps",
    "a_crun_srps",
    *_cell_columns("ffsrps", _MONETARY_REPO_HOLDERS),
    "a_mmf_rsrps",
    "a_depinst_rsrps",
    "a_brok_rsrps",
    "a_gse_rsrps",
    "a_tot_mmf",
    *_cell_columns("mmf", _MMF_HOLDERS),
    "a_tot_mufu",
    *_cell_columns("mufu", _MUTUAL_FUND_HOLDERS),
    *_MUTUAL_FUND_RAW_COLUMNS,
    "d_pdi_timdep",
    "d_pdi_chkdep",
    "d_pdi_bnd_hold",
    "d_pdi_cpap_hold",
    "d_pdinet_equity",
    *_cell_columns("timdep", _TIME_DEPOSIT_HOLDERS),
    *_cell_columns("chkdep", _CHECK_DEPOSIT_HOLDERS),
    *_cell_columns("pdibnd", _PDI_BOND_HOLDERS),
    *_cell_columns("pdicpap", _PDI_CP_HOLDERS),
    *_cell_columns("pdiequity", _PDI_EQUITY_HOLDERS),
    "d_nfcnet_cpap",
    "d_nfcnet_bnd",
    "d_nfcnet_equity",
    "d_nfc_othl",
    "d_nfcnet_fdi",
    "d_nfc_tax",
    "d_nfc_dinl",
    "d_nfc_mort",
    "d_nfcnet_trapay",
    "d_nfc_misc",
    *_cell_columns("nfccpap", _NFC_CP_HOLDERS),
    *_cell_columns("nfcbnd", _NFC_BOND_HOLDERS),
    *_cell_columns("nfcequity", _NFC_EQUITY_HOLDERS),
    *_cell_columns("nfcothl", _NFC_OTHER_LOAN_HOLDERS),
    "d_nfnc_othl",
    "d_nfnc_fdi",
    "d_nfnc_tax",
    "d_nfnc_dinl",
    "d_nfnc_mort",
    "d_nfncnet_trapay",
    "d_nfnc_misc",
    "d_nfnc_equity",
    "a_fgov_nfncothl",
    "a_gse_nfncothl",
    "a_finc_nfncothl",
    "fl153090005q",
    "fl514190005q",
)

if len(DIRECT_SOURCE_COLUMNS) != len(set(DIRECT_SOURCE_COLUMNS)):
    raise RuntimeError("2021 direct-cell source contract contains duplicates")
if any(_PROHIBITED_SOURCE.search(column) for column in DIRECT_SOURCE_COLUMNS):
    raise RuntimeError("2021 direct-cell contract includes a seven-round output")


@dataclass(frozen=True, slots=True)
class Position:
    """One completed direct position in millions of current dollars."""

    holder: str
    value: float
    household_class: str
    source: str


@dataclass(frozen=True, slots=True)
class ComponentDiagnostics:
    """Accounting diagnostics for one issuer-instrument component."""

    year: int
    intermediary: str
    component: str
    liability_margin_millions: float
    allocated_millions: float
    negative_cells: int
    negative_abs_millions: float
    fallback_to_unassigned: bool


def load_2021_direct_cells(path: Path) -> pd.DataFrame:
    """Load only pre-unveiling direct cells from ``Yunveilhhd.dta``.

    Parameters
    ----------
    path
        Immutable authors-kit file produced by the direct-cell construction
        and seven-round Stata program.

    Returns
    -------
    pandas.DataFrame
        One validated row per year, 1963--2016.  The selected columns contain
        direct positions, issuer margins, primary household debt, and raw
        mutual-fund portfolio inputs.  No round or final unveiled field is
        selected.
    """

    frame = pd.read_stata(
        path,
        columns=list(DIRECT_SOURCE_COLUMNS),
        convert_categoricals=False,
    )
    years = pd.to_numeric(frame["year"], errors="raise")
    if years.isna().any() or not np.allclose(years, np.rint(years)):
        raise ValueError("2021 direct cells: year must contain finite integers")
    frame["year"] = np.rint(years).astype(np.int16)
    frame = frame.loc[frame["year"].between(1963, 2016)].copy()
    if frame["year"].duplicated().any():
        raise ValueError("2021 direct cells: duplicate annual keys")
    if frame["year"].tolist() != list(range(1963, 2017)):
        raise ValueError("2021 direct cells: incomplete 1963--2016 sample")
    numeric = list(DIRECT_SOURCE_COLUMNS[1:])
    frame[numeric] = frame[numeric].astype(np.float64)
    frame[list(_STRUCTURAL_ZERO_COLUMNS)] = frame[
        list(_STRUCTURAL_ZERO_COLUMNS)
    ].fillna(0.0)
    if not np.isfinite(frame[numeric].to_numpy()).all():
        bad = frame[numeric].columns[frame[numeric].isna().any()].tolist()
        # The only structural missings allowed are the pre-1991 detailed
        # mutual-fund portfolio series reconstructed below.
        allowed = set(_MUTUAL_FUND_RAW_COLUMNS[:-1])
        if set(bad) - allowed:
            raise ValueError(f"2021 direct cells: unexpected missing fields {bad}")
    return frame.reset_index(drop=True)


def construct_2021_direct_full_leontief(
    direct_cells: pd.DataFrame,
    distributional_shares: pd.DataFrame,
    national_income: pd.DataFrame,
    *,
    start_year: int = 1963,
    end_year: int = 2016,
    base_year: int = 1982,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    r"""Construct Figure 8 from 2021 direct cells and a full network solve.

    The matrix rows are liability issuers and columns are direct holders.  For
    each year, household-holder cells are expanded into four DINA wealth-group
    columns before direct rows are normalized.  Writing those intermediary
    rows as ``[B_t, Q_t]``, ultimate ownership is

    .. math::

       \Omega_t=(I-Q_t)^{-1}B_t.

    Returns
    -------
    result, diagnostics, component_diagnostics : tuple of pandas.DataFrame
        Annual Figure 8 series, annual network/accounting checks, and a long
        issuer-component audit of the reconstructed direct rows.
    """

    years = list(range(start_year, end_year + 1))
    if start_year > end_year or base_year not in years:
        raise ValueError("2021-direct Figure 8 sample must contain the base year")
    cells = direct_cells.loc[direct_cells["year"].between(start_year, end_year)]
    shares = distributional_shares.loc[
        distributional_shares["year"].between(start_year, end_year)
    ]
    income = national_income.loc[
        national_income["year"].between(start_year, end_year)
    ]
    for label, frame in (
        ("2021 direct cells", cells),
        ("DINA shares", shares),
        ("national income", income),
    ):
        if frame["year"].tolist() != years:
            missing = sorted(set(years) - set(frame["year"]))
            raise ValueError(f"{label}: incomplete annual sample; missing={missing}")

    mutual_fund_weights = _reconstruct_mutual_fund_weights(cells)
    share_lookup = shares.set_index("year")
    weight_lookup = mutual_fund_weights.set_index("year")
    annual_rows: list[dict[str, float | int]] = []
    diagnostic_rows: list[dict[str, float | int]] = []
    component_rows: list[dict[str, float | int | bool | str]] = []
    for record in cells.itertuples(index=False, name=None):
        row = pd.Series(record, index=cells.columns)
        year = int(row["year"])
        annual, diagnostics, components = _construct_annual_result(
            row,
            share_lookup.loc[year],
            weight_lookup.loc[year],
            year=year,
        )
        annual_rows.append(annual)
        diagnostic_rows.append(diagnostics)
        component_rows.extend(asdict(component) for component in components)

    result = _scale_and_normalize(
        pd.DataFrame(annual_rows),
        income,
        base_year=base_year,
    )
    diagnostics = pd.DataFrame(diagnostic_rows).sort_values("year").reset_index(
        drop=True
    )
    component_diagnostics = (
        pd.DataFrame(component_rows)
        .sort_values(["year", "intermediary", "component"])
        .reset_index(drop=True)
    )
    return result, diagnostics, component_diagnostics


def _construct_annual_result(
    row: pd.Series,
    share_row: pd.Series,
    mutual_fund_weights: pd.Series,
    *,
    year: int,
) -> tuple[
    dict[str, float | int],
    dict[str, float | int],
    list[ComponentDiagnostics],
]:
    """Construct and solve one year's coarsened 2021 direct network."""

    row_positions, components = _build_intermediary_positions(row, year=year)
    owner_levels: dict[str, dict[str, float]] = {}
    for intermediary, positions in row_positions.items():
        owner_levels[intermediary] = _allocate_positions(
            positions,
            share_row,
            mutual_fund_weights,
        )

    row_totals = {
        intermediary: sum(levels.values())
        for intermediary, levels in owner_levels.items()
    }
    active = [name for name in INTERMEDIARIES if row_totals[name] > 1e-8]
    inactive = set(INTERMEDIARIES) - set(active)
    for levels in owner_levels.values():
        for intermediary in inactive:
            amount = levels.pop(intermediary, 0.0)
            if amount:
                levels["unassigned"] = levels.get("unassigned", 0.0) + amount

    destinations = [*OWNERS, *active]
    levels = np.array(
        [
            [owner_levels[issuer].get(destination, 0.0) for destination in destinations]
            for issuer in active
        ],
        dtype=float,
    )
    if not np.isfinite(levels).all() or (levels < -1e-10).any():
        raise ValueError(f"{year}: reconstructed direct matrix is invalid")
    totals = levels.sum(axis=1)
    if (totals <= 0.0).any():
        raise ValueError(f"{year}: active intermediary has no positive liabilities")
    direct = levels / totals[:, None]
    owner_block = direct[:, : len(OWNERS)]
    cross_block = direct[:, len(OWNERS) :]
    spectral_radius = float(np.max(np.abs(np.linalg.eigvals(cross_block))))
    if spectral_radius >= 1.0 - 1e-10:
        raise ValueError(f"{year}: 2021 direct intermediary chains do not converge")
    omega = np.linalg.solve(np.eye(len(active)) - cross_block, owner_block)
    omega_row_error = float(np.max(np.abs(omega.sum(axis=1) - 1.0)))
    if omega_row_error > 1e-9:
        raise ValueError(f"{year}: unveiled ownership rows do not close")

    debt_positions, debt_components = _build_household_debt_positions(row, year=year)
    components.extend(debt_components)
    category_owner_levels: dict[str, FloatArray] = {}
    category_totals: dict[str, float] = {}
    category_primary_errors: dict[str, float] = {}
    for category, positions in debt_positions.items():
        direct_category = _allocate_positions(
            positions,
            share_row,
            mutual_fund_weights,
        )
        category_vector = np.array(
            [direct_category.get(destination, 0.0) for destination in destinations],
            dtype=float,
        )
        inactive_category = sum(
            direct_category.get(name, 0.0) for name in inactive
        )
        if inactive_category > 1e-6:
            category_vector[OWNERS.index("unassigned")] += inactive_category
        category_total = float(category_vector.sum())
        if category_total <= 0.0:
            raise ValueError(f"{year}: {category} has no positive debt margin")
        final_owner_levels = (
            category_vector[len(OWNERS) :] @ omega
            + category_vector[: len(OWNERS)]
        )
        category_error = float(
            abs(final_owner_levels.sum() - category_total) / category_total
        )
        if category_error > 1e-9:
            raise ValueError(f"{year}: {category} owner allocation does not close")
        category_owner_levels[category] = final_owner_levels
        category_totals[category] = category_total
        category_primary_errors[category] = category_error

    total_debt = sum(category_totals.values())
    expected_debt = float(row["d_hh_hmort"] + row["d_hh_ccred"])
    if not np.isclose(total_debt, expected_debt, atol=1e-4, rtol=1e-9):
        raise ValueError(f"{year}: direct household-debt positions do not close")
    source_debt_error = abs(float(row["a_hhd_tot"]) - expected_debt)
    if source_debt_error / expected_debt > 1e-6:
        raise ValueError(f"{year}: authors-kit household-debt margins do not close")
    final_owner_levels = sum(category_owner_levels.values())
    final_share = final_owner_levels / total_debt
    primary_error = float(
        abs(final_owner_levels.sum() - total_debt) / total_debt
    )
    if primary_error > 1e-9:
        raise ValueError(f"{year}: household-debt owner allocation does not close")

    category_liability_specs = {
        "home_mortgage": (float(row["d_hh_hmort"]), "ownermort"),
        "consumer_credit": (float(row["d_hh_ccred"]), "nonmort"),
    }
    output: dict[str, float | int] = {
        "year": year,
        "household_debt_millions": total_debt,
        "authors_source_debt_margin_error_millions": source_debt_error,
    }
    for group_index, group in enumerate(GROUPS):
        assets = 0.0
        liabilities = 0.0
        for category, (category_total, share_class) in (
            category_liability_specs.items()
        ):
            category_assets = float(category_owner_levels[category][group_index])
            category_liabilities = category_total * float(
                share_row[f"{share_class}_{group}"]
            )
            output[f"debt_assets_{category}_{group}_millions"] = category_assets
            output[
                f"debt_liabilities_{category}_{group}_millions"
            ] = category_liabilities
            output[f"net_debt_{category}_{group}_millions"] = (
                category_assets - category_liabilities
            )
            assets += category_assets
            liabilities += category_liabilities
        output[f"debt_assets_{group}_millions"] = assets
        output[f"debt_liabilities_{group}_millions"] = liabilities
        output[f"net_debt_{group}_millions"] = assets - liabilities
    for measure in ("debt_assets", "debt_liabilities", "net_debt"):
        output[f"{measure}_bottom_99_millions"] = sum(
            float(output[f"{measure}_{group}_millions"])
            for group in ("next_9", "next_40", "bottom_50")
        )
        for category in DEBT_CATEGORIES:
            output[f"{measure}_{category}_bottom_99_millions"] = sum(
                float(output[f"{measure}_{category}_{group}_millions"])
                for group in ("next_9", "next_40", "bottom_50")
            )

    component_negative_cells = sum(item.negative_cells for item in components)
    component_negative_abs = sum(item.negative_abs_millions for item in components)
    liability_error = abs(
        sum(float(output[f"debt_liabilities_{group}_millions"]) for group in GROUPS)
        - total_debt
    )
    category_liability_error = max(
        abs(
            sum(
                float(output[f"debt_liabilities_{category}_{group}_millions"])
                for group in GROUPS
            )
            - category_totals[category]
        )
        for category in DEBT_CATEGORIES
    )
    category_additivity_error = max(
        abs(
            float(output[f"{measure}_{group}_millions"])
            - sum(
                float(output[f"{measure}_{category}_{group}_millions"])
                for category in DEBT_CATEGORIES
            )
        )
        for measure in ("debt_assets", "debt_liabilities", "net_debt")
        for group in GROUPS
    )
    diagnostics: dict[str, float | int] = {
        "year": year,
        "source_direct_variables": len(DIRECT_SOURCE_COLUMNS) - 1,
        "round_variables_read": 0,
        "coarsened_intermediaries": len(INTERMEDIARIES),
        "active_intermediaries": len(active),
        "ultimate_owner_columns": len(OWNERS),
        "negative_direct_cells_clipped": component_negative_cells,
        "negative_direct_abs_millions": component_negative_abs,
        "negative_direct_abs_share_of_debt": component_negative_abs / total_debt,
        "spectral_radius": spectral_radius,
        "direct_row_sum_max_error": float(
            np.max(np.abs(direct.sum(axis=1) - 1.0))
        ),
        "omega_row_sum_max_error": omega_row_error,
        "omega_minimum_share": float(omega.min()),
        "primary_asset_sum_error": primary_error,
        "category_primary_asset_sum_max_error": max(
            category_primary_errors.values()
        ),
        "primary_minimum_share": float(final_share.min()),
        "liability_sum_error_millions": liability_error,
        "category_liability_sum_max_error_millions": category_liability_error,
        "category_additivity_max_error_millions": category_additivity_error,
        "authors_source_debt_margin_error_millions": source_debt_error,
        "unassigned_ultimate_debt_share": float(
            final_share[OWNERS.index("unassigned")]
        ),
        "home_mortgage_unassigned_ultimate_share": float(
            category_owner_levels["home_mortgage"][OWNERS.index("unassigned")]
            / category_totals["home_mortgage"]
        ),
        "consumer_credit_unassigned_ultimate_share": float(
            category_owner_levels["consumer_credit"][OWNERS.index("unassigned")]
            / category_totals["consumer_credit"]
        ),
        "mutual_fund_equity_share": float(mutual_fund_weights["equity"]),
        "mutual_fund_taxbond_share": float(mutual_fund_weights["taxbond"]),
        "mutual_fund_muni_share": float(mutual_fund_weights["muni"]),
        "household_debt_millions": total_debt,
    }
    return output, diagnostics, components


def _build_intermediary_positions(
    row: pd.Series,
    *,
    year: int,
) -> tuple[dict[str, list[Position]], list[ComponentDiagnostics]]:
    """Reconstruct eight direct issuer rows from authors-kit completed cells."""

    rows = {name: [] for name in INTERMEDIARIES}
    diagnostics: list[ComponentDiagnostics] = []

    def add(
        issuer: str,
        component: str,
        target: float,
        variables: Mapping[str, str],
        household_class: str,
    ) -> None:
        positions, audit = _scaled_component(
            row,
            variables,
            target,
            household_class,
            year=year,
            intermediary=issuer,
            component=component,
        )
        rows[issuer].extend(positions)
        diagnostics.append(audit)

    add(
        "mortgage_complex",
        "gse_securities",
        row["d_master_gsesec"],
        {f"a_{holder}_gsegsesec": holder for holder in _GSE_SECURITY_HOLDERS},
        "taxbond",
    )
    for prefix, margin in (
        ("absbnd", "d_absnet_bnd"),
        ("fincbnd", "d_fincnet_bnd"),
        ("mreitbnd", "d_mreitnet_bnd"),
    ):
        add(
            "mortgage_complex",
            prefix,
            row[margin],
            {f"a_{holder}_{prefix}": holder for holder in _INTERMEDIARY_BOND_HOLDERS},
            "taxbond",
        )
    add(
        "mortgage_complex",
        "commercial_paper",
        row["d_master_cpap"],
        {f"a_{holder}_cpap": holder for holder in _COMMERCIAL_PAPER_HOLDERS},
        "taxbond",
    )
    add(
        "mortgage_complex",
        "mortgage_reit_residual",
        row["d_mreit_resid"],
        {"d_mreit_resid": "unassigned"},
        "taxbond",
    )

    add(
        "monetary_authority",
        "depository_reserves_and_vault_cash",
        row["d_mone_dpires"] + row["d_mone_dpicsh"],
        {"d_mone_dpires": "pdi", "d_mone_dpicsh": "pdi"},
        "taxbond",
    )
    add(
        "monetary_authority",
        "foreign_currency",
        row["d_mone_dforiegn"],
        {"d_mone_dforiegn": "row"},
        "currency",
    )
    currency_variables = {
        f"a_{holder}_chkcur": holder for holder in _MONETARY_CURRENCY_HOLDERS
    }
    currency_variables["a_row_cur"] = "row"
    add(
        "monetary_authority",
        "domestic_currency",
        row["d_mone_curnb"],
        currency_variables,
        "currency",
    )
    repo_variables = {
        "a_depinst_netsrps": "depinst",
        "a_fbank_netsrps": "fbank",
        "a_crun_srps": "crun",
        **{
            f"a_{holder}_ffsrps": holder
            for holder in _MONETARY_REPO_HOLDERS
        },
    }
    add(
        "monetary_authority",
        "security_repurchase_agreements",
        row["d_mone_srps"],
        repo_variables,
        "taxbond",
    )
    add(
        "monetary_authority",
        "reverse_repurchase_agreements",
        row["d_mone_rsrps"],
        {
            "a_mmf_rsrps": "mmf",
            "a_depinst_rsrps": "depinst",
            "a_brok_rsrps": "brok",
            "a_gse_rsrps": "gse",
        },
        "taxbond",
    )
    add(
        "monetary_authority",
        "residual_liabilities",
        row["d_mone_resid"],
        {"d_mone_resid": "unassigned"},
        "taxbond",
    )

    add(
        "money_market_funds",
        "money_market_fund_shares",
        row["a_tot_mmf"],
        {f"a_{holder}_mmf": holder for holder in _MMF_HOLDERS},
        "taxbond",
    )
    add(
        "mutual_funds",
        "mutual_fund_shares",
        row["a_tot_mufu"],
        {f"a_{holder}_mufu": holder for holder in _MUTUAL_FUND_HOLDERS},
        "mutual_fund",
    )

    for component, target, holders, class_name in (
        ("time_deposits", "d_pdi_timdep", _TIME_DEPOSIT_HOLDERS, "taxbond"),
        ("checkable_deposits", "d_pdi_chkdep", _CHECK_DEPOSIT_HOLDERS, "currency"),
        ("bonds", "d_pdi_bnd_hold", _PDI_BOND_HOLDERS, "taxbond"),
        ("commercial_paper", "d_pdi_cpap_hold", _PDI_CP_HOLDERS, "taxbond"),
        ("equity", "d_pdinet_equity", _PDI_EQUITY_HOLDERS, "equity"),
    ):
        suffix = {
            "time_deposits": "timdep",
            "checkable_deposits": "chkdep",
            "bonds": "pdibnd",
            "commercial_paper": "pdicpap",
            "equity": "pdiequity",
        }[component]
        add(
            "private_depositories",
            component,
            row[target],
            {f"a_{holder}_{suffix}": holder for holder in holders},
            class_name,
        )

    for component, target, holders, suffix, class_name in (
        ("commercial_paper", "d_nfcnet_cpap", _NFC_CP_HOLDERS, "nfccpap", "taxbond"),
        ("bonds", "d_nfcnet_bnd", _NFC_BOND_HOLDERS, "nfcbnd", "taxbond"),
        ("equity", "d_nfcnet_equity", _NFC_EQUITY_HOLDERS, "nfcequity", "equity"),
        ("other_loans", "d_nfc_othl", _NFC_OTHER_LOAN_HOLDERS, "nfcothl", "equity"),
    ):
        add(
            "nonfinancial_corporate",
            component,
            row[target],
            {f"a_{holder}_{suffix}": holder for holder in holders},
            class_name,
        )
    add(
        "nonfinancial_corporate",
        "foreign_direct_investment",
        row["d_nfcnet_fdi"],
        {"d_nfcnet_fdi": "row"},
        "equity",
    )
    add(
        "nonfinancial_corporate",
        "taxes_payable",
        row["d_nfc_tax"],
        {"d_nfc_tax": "fgov"},
        "taxbond",
    )
    nfc_residual = sum(
        max(float(row[column]), 0.0)
        for column in (
            "d_nfc_dinl", "d_nfc_mort", "d_nfcnet_trapay", "d_nfc_misc"
        )
    )
    add(
        "nonfinancial_corporate",
        "unidentified_liabilities",
        nfc_residual,
        {"d_nfc_dinl": "unassigned", "d_nfc_mort": "unassigned",
         "d_nfcnet_trapay": "unassigned", "d_nfc_misc": "unassigned"},
        "taxbond",
    )

    add(
        "nonfinancial_noncorporate",
        "other_loans",
        row["d_nfnc_othl"],
        {
            "a_fgov_nfncothl": "fgov",
            "a_gse_nfncothl": "gse",
            "a_finc_nfncothl": "finc",
        },
        "taxbond",
    )
    add(
        "nonfinancial_noncorporate",
        "foreign_direct_investment",
        row["d_nfnc_fdi"],
        {"d_nfnc_fdi": "row"},
        "business",
    )
    add(
        "nonfinancial_noncorporate",
        "taxes_payable",
        row["d_nfnc_tax"],
        {"d_nfnc_tax": "fgov"},
        "taxbond",
    )
    add(
        "nonfinancial_noncorporate",
        "noncorporate_equity",
        row["d_nfnc_equity"],
        {"d_nfnc_equity": "hh"},
        "business",
    )
    nfnc_residual = sum(
        max(float(row[column]), 0.0)
        for column in (
            "d_nfnc_dinl", "d_nfnc_mort", "d_nfncnet_trapay", "d_nfnc_misc"
        )
    )
    add(
        "nonfinancial_noncorporate",
        "unidentified_liabilities",
        nfnc_residual,
        {"d_nfnc_dinl": "unassigned", "d_nfnc_mort": "unassigned",
         "d_nfncnet_trapay": "unassigned", "d_nfnc_misc": "unassigned"},
        "taxbond",
    )

    pins_total = max(float(row["fl514190005q"]), 0.0)
    pins_household = min(max(float(row["fl153090005q"]), 0.0), pins_total)
    add(
        "property_casualty_insurance",
        "household_and_residual_claims",
        pins_total,
        {"fl153090005q": "hh", "fl514190005q": "unassigned"},
        "taxbond",
    )
    # The generic scaler would otherwise count the full liability total as an
    # unassigned weight.  Replace this row with the old program's exact
    # household-claim fraction and a residual owner.
    rows["property_casualty_insurance"] = [
        Position("hh", pins_household, "taxbond", "fl153090005q"),
        Position(
            "unassigned",
            pins_total - pins_household,
            "taxbond",
            "fl514190005q-fl153090005q",
        ),
    ]
    diagnostics[-1] = ComponentDiagnostics(
        year=year,
        intermediary="property_casualty_insurance",
        component="household_and_residual_claims",
        liability_margin_millions=pins_total,
        allocated_millions=pins_total,
        negative_cells=int(row["fl153090005q"] < 0 or row["fl514190005q"] < 0),
        negative_abs_millions=float(
            max(-row["fl153090005q"], 0.0) + max(-row["fl514190005q"], 0.0)
        ),
        fallback_to_unassigned=False,
    )
    return rows, diagnostics


def _build_household_debt_positions(
    row: pd.Series,
    *,
    year: int,
) -> tuple[dict[str, list[Position]], list[ComponentDiagnostics]]:
    """Construct direct holder positions for mortgages and consumer credit."""

    output: dict[str, list[Position]] = {}
    diagnostics: list[ComponentDiagnostics] = []
    for category, component, target, holders, suffix in (
        (
            "home_mortgage",
            "household_home_mortgages",
            row["d_hh_hmort"],
            _HOUSEHOLD_MORTGAGE_HOLDERS,
            "hmort",
        ),
        (
            "consumer_credit",
            "household_consumer_credit",
            row["d_hh_ccred"],
            _HOUSEHOLD_CONSUMER_CREDIT_HOLDERS,
            "ccred",
        ),
    ):
        positions, audit = _scaled_component(
            row,
            {f"a_{holder}_{suffix}": holder for holder in holders},
            target,
            "taxbond",
            year=year,
            intermediary="household_primary_debt",
            component=component,
        )
        output[category] = positions
        diagnostics.append(audit)
    return output, diagnostics


def _scaled_component(
    row: pd.Series,
    variables: Mapping[str, str],
    target: float,
    household_class: str,
    *,
    year: int,
    intermediary: str,
    component: str,
) -> tuple[list[Position], ComponentDiagnostics]:
    """Clip direct weights and balance them to one issuer-component margin."""

    margin = max(float(target), 0.0)
    raw = np.array([float(row[column]) for column in variables], dtype=float)
    negative = raw < 0.0
    clipped = np.clip(raw, 0.0, None)
    fallback = False
    if margin <= 0.0:
        positions: list[Position] = []
    elif clipped.sum() <= 0.0:
        positions = [Position("unassigned", margin, household_class, component)]
        fallback = True
    else:
        scale = margin / clipped.sum()
        positions = [
            Position(holder, value * scale, household_class, column)
            for (column, holder), value in zip(variables.items(), clipped, strict=True)
            if value > 0.0
        ]
    allocated = sum(item.value for item in positions)
    if not np.isclose(allocated, margin, atol=1e-5, rtol=1e-10):
        raise ValueError(f"{year}: {intermediary}/{component} does not balance")
    diagnostics = ComponentDiagnostics(
        year=year,
        intermediary=intermediary,
        component=component,
        liability_margin_millions=margin,
        allocated_millions=allocated,
        negative_cells=int(negative.sum()),
        negative_abs_millions=float(-raw[negative].sum()),
        fallback_to_unassigned=fallback,
    )
    return positions, diagnostics


def _allocate_positions(
    positions: Iterable[Position],
    share_row: pd.Series,
    mutual_fund_weights: pd.Series,
) -> dict[str, float]:
    """Map old-kit holder aliases into owner and intermediary destinations."""

    levels: dict[str, float] = {}
    for position in positions:
        if position.value <= 0.0:
            continue
        holder = position.holder
        if holder in {"hh", "lins", "pens", "govret"}:
            class_name = "pens" if holder in {"lins", "pens", "govret"} else position.household_class
            distribution = _distribution_vector(
                share_row,
                class_name,
                mutual_fund_weights,
            )
            for group, share in zip(GROUPS, distribution, strict=True):
                levels[group] = levels.get(group, 0.0) + position.value * share
            continue
        destination = _holder_destination(holder)
        levels[destination] = levels.get(destination, 0.0) + position.value
    return levels


def _holder_destination(holder: str) -> str:
    """Return the coarsened network destination for one old-kit alias."""

    mapping = {
        "fgov": "federal_government",
        "lgov": "state_local_government",
        "row": "rest_of_world",
        "fdi": "rest_of_world",
        "nfc": "nonfinancial_corporate",
        "nfnc": "nonfinancial_noncorporate",
        "mone": "monetary_authority",
        "mmf": "money_market_funds",
        "mufu": "mutual_funds",
        "pdi": "private_depositories",
        "depinst": "private_depositories",
        "fbank": "private_depositories",
        "busaf": "private_depositories",
        "crun": "private_depositories",
        "pins": "property_casualty_insurance",
        "gse": "mortgage_complex",
        "agpool": "mortgage_complex",
        "abs": "mortgage_complex",
        "finc": "mortgage_complex",
        "mreit": "mortgage_complex",
        "ereit": "mortgage_complex",
        "reit": "mortgage_complex",
        "unassigned": "unassigned",
    }
    return mapping.get(holder, "unassigned")


def _distribution_vector(
    share_row: pd.Series,
    class_name: str,
    mutual_fund_weights: pd.Series,
) -> FloatArray:
    """Return four DINA group shares for one old-kit household claim."""

    if class_name == "business":
        class_name = "bus"
    if class_name == "mutual_fund":
        vector = sum(
            float(mutual_fund_weights[component])
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
    return vector / vector.sum()


def _reconstruct_mutual_fund_weights(cells: pd.DataFrame) -> pd.DataFrame:
    """Reproduce the old Stata mutual-fund equity/bond/muni split.

    Detailed portfolio categories begin in 1991.  For earlier years, the old
    program linearly interpolates/extrapolates the detailed equity share over
    the aggregate mutual-fund equity ratio, then allocates the non-equity
    remainder between taxable and municipal bonds at the observed mean ratio.
    """

    denominator = cells["lm654090000q"] - cells["lm654091403q"]
    equity = (cells["lm654091603q"] + cells["lm654092603q"]) / denominator
    taxbond = (
        cells["lm654091303q"]
        + cells["lm654091203q"]
        - cells["lm653062003q"]
    ) / denominator
    muni = cells["lm653062003q"] / denominator
    total = equity + taxbond + muni
    equity = equity / total
    taxbond = taxbond / total
    muni = muni / total
    proxy = cells["lm653064100q"] / cells["lm654090000q"]
    observed = equity.notna() & proxy.notna()
    if observed.sum() < 2:
        raise ValueError("mutual-fund split: insufficient observed portfolio years")
    x = proxy.loc[observed].to_numpy(dtype=float)
    y = equity.loc[observed].to_numpy(dtype=float)
    order = np.argsort(x)
    x = x[order]
    y = y[order]
    missing = equity.isna()
    equity.loc[missing] = [
        _linear_interpolate_extrapolate(float(value), x, y)
        for value in proxy.loc[missing]
    ]
    bond_ratio = float((taxbond / (taxbond + muni)).mean(skipna=True))
    taxbond.loc[taxbond.isna()] = (1.0 - equity.loc[taxbond.isna()]) * bond_ratio
    muni = 1.0 - equity - taxbond
    result = pd.DataFrame(
        {
            "year": cells["year"].to_numpy(),
            "equity": equity.to_numpy(dtype=float),
            "taxbond": taxbond.to_numpy(dtype=float),
            "muni": muni.to_numpy(dtype=float),
        }
    )
    values = result[["equity", "taxbond", "muni"]]
    if not np.isfinite(values.to_numpy()).all() or (values < -1e-10).any().any():
        raise ValueError("mutual-fund split: invalid reconstructed weights")
    if (values.sum(axis=1) - 1.0).abs().max() > 1e-10:
        raise ValueError("mutual-fund split: weights do not sum to one")
    return result


def _linear_interpolate_extrapolate(
    value: float,
    x: FloatArray,
    y: FloatArray,
) -> float:
    """Match Stata ``ipolate ..., epolate`` for a scalar point."""

    if value < x[0]:
        return float(y[0] + (value - x[0]) * (y[1] - y[0]) / (x[1] - x[0]))
    if value > x[-1]:
        return float(
            y[-1]
            + (value - x[-1]) * (y[-1] - y[-2]) / (x[-1] - x[-2])
        )
    return float(np.interp(value, x, y))


def _scale_and_normalize(
    frame: pd.DataFrame,
    national_income: pd.DataFrame,
    *,
    base_year: int,
) -> pd.DataFrame:
    """Scale net-debt stocks by national income and subtract the 1982 ratio."""

    output = frame.merge(
        national_income,
        on="year",
        how="left",
        validate="one_to_one",
        indicator=True,
    )
    if not output["_merge"].eq("both").all():
        raise ValueError("2021-direct Figure 8: unmatched national-income year")
    output = output.drop(columns="_merge")
    for group in DISPLAY_GROUPS:
        for measure in ("debt_assets", "debt_liabilities", "net_debt"):
            ratio = output[f"{measure}_{group}_millions"] / output[
                "national_income_millions"
            ]
            base = ratio.loc[output["year"] == base_year]
            if len(base) != 1:
                raise ValueError(f"2021-direct Figure 8: missing unique {base_year}")
            output[f"{measure}_{group}_to_national_income"] = ratio
            output[f"{measure}_{group}_relative_to_{base_year}"] = (
                ratio - base.iloc[0]
            )
            for category in DEBT_CATEGORIES:
                category_ratio = output[
                    f"{measure}_{category}_{group}_millions"
                ] / output["national_income_millions"]
                category_base = category_ratio.loc[output["year"] == base_year]
                output[
                    f"{measure}_{category}_{group}_to_national_income"
                ] = category_ratio
                output[
                    f"{measure}_{category}_{group}_relative_to_{base_year}"
                ] = category_ratio - category_base.iloc[0]
    return output.sort_values("year").reset_index(drop=True)


def build_debt_composition_panel(
    full_leontief_result: pd.DataFrame,
    *,
    base_year: int = 1982,
) -> pd.DataFrame:
    """Reshape category-specific Figure 8 stocks into a validated long panel.

    Parameters
    ----------
    full_leontief_result
        Wide annual output from :func:`construct_2021_direct_full_leontief`.
        Monetary values are millions of current dollars; ratios are fractions
        of national income.
    base_year
        Base year already used to normalize the wide result.

    Returns
    -------
    pandas.DataFrame
        One row per year, debt category, and wealth group.  The primary key is
        ``(year, category, group)``. Liabilities are positive amounts owed.
    """

    records: list[dict[str, float | int | str]] = []
    for row in full_leontief_result.itertuples(index=False):
        values = row._asdict()
        for category in DEBT_CATEGORIES:
            for group in DISPLAY_GROUPS:
                record: dict[str, float | int | str] = {
                    "year": int(values["year"]),
                    "category": category,
                    "group": group,
                    "national_income_millions": float(
                        values["national_income_millions"]
                    ),
                }
                for measure in ("debt_assets", "debt_liabilities", "net_debt"):
                    prefix = f"{measure}_{category}_{group}"
                    record[f"{measure}_millions"] = float(
                        values[f"{prefix}_millions"]
                    )
                    record[f"{measure}_to_national_income"] = float(
                        values[f"{prefix}_to_national_income"]
                    )
                    record[f"{measure}_relative_to_{base_year}"] = float(
                        values[f"{prefix}_relative_to_{base_year}"]
                    )
                records.append(record)
    output = pd.DataFrame(records).sort_values(
        ["year", "category", "group"]
    ).reset_index(drop=True)
    if output.duplicated(["year", "category", "group"]).any():
        raise ValueError("debt composition: duplicate year-category-group keys")
    expected_rows = len(full_leontief_result) * len(DEBT_CATEGORIES) * len(
        DISPLAY_GROUPS
    )
    if len(output) != expected_rows:
        raise ValueError("debt composition: incomplete long-panel reshape")
    return output


__all__ = [
    "DIRECT_SOURCE_COLUMNS",
    "DEBT_CATEGORIES",
    "INTERMEDIARIES",
    "OWNERS",
    "build_debt_composition_panel",
    "construct_2021_direct_full_leontief",
    "load_2021_direct_cells",
    "load_authors_national_income",
    "load_distributional_shares",
]
