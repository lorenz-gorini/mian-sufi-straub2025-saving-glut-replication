"""Newer-public-data robustness construction for the 2025 Figure 1 object.

The figure measures the household financial claims that sit behind the
intermediation veil.  In FWTW data these are claims held by households and
issued by financial intermediaries.  They are observed direct claims on an
intermediary, but indirect claims on the primary assets that the intermediary
finances.  This object is therefore not ``Omega - M_bar``.

This module deliberately does not read the authors' replication kit.  It uses
the pinned June 2026 public FWTW release and BEA national income distributed by
FRED.  Its output is secondary, newer-vintage robustness evidence.  The
primary old-input reconstruction is implemented separately in
``unveiling.figure1_authors``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


_FWTW_COLUMNS = [
    "Instrument Name",
    "Instrument Code",
    "Holder Name",
    "Holder Code",
    "Issuer Name",
    "Issuer Code",
    "Date",
    "Level",
]
_FWTW_KEY = ["Instrument Code", "Holder Code", "Issuer Code", "Date"]


@dataclass(frozen=True, slots=True)
class Figure1Definition:
    """Sector-code definition of indirect household financial ownership.

    The codes follow the Federal Reserve's FWTW release.  Households are the
    holder of interest.  Claims issued by the four ultimate-owner sectors and
    the two nonfinancial business sectors do not constitute claims on a
    financial intermediary.  Rest-of-world claims are also excluded from the
    denominator because Figure 1 concerns U.S. financial assets.
    """

    household: int = 15
    state_local_government: int = 21
    rest_of_world: int = 26
    federal_government: int = 31
    nonfinancial_issuers: tuple[int, int] = (10, 11)
    total_sector: int = 89
    discrepancy_sector: int = 90

    @property
    def nonintermediary_issuers(self) -> tuple[int, ...]:
        """Return issuer codes that are not financial intermediaries."""

        return (
            *self.nonfinancial_issuers,
            self.household,
            self.state_local_government,
            self.rest_of_world,
            self.federal_government,
            self.total_sector,
            self.discrepancy_sector,
        )


def read_fwtw(path: str | Path) -> pd.DataFrame:
    """Read and validate a Federal Reserve FWTW long-form CSV.

    Parameters
    ----------
    path
        CSV with one row per instrument-holder-issuer-quarter relationship.
        ``Level`` is a stock in millions of current dollars.

    Returns
    -------
    pandas.DataFrame
        Validated FWTW observations with the published column names.

    Raises
    ------
    FileNotFoundError
        If ``path`` does not exist.
    ValueError
        If required columns, keys, dates, or code-name mappings are invalid.

    Notes
    -----
    The official FWTW technical note permits negative levels for net positions
    and historical data imperfections.  This loader therefore preserves them.
    """

    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"FWTW file not found: {source}")

    data = pd.read_csv(
        source,
        usecols=_FWTW_COLUMNS,
        dtype={
            "Instrument Name": "string",
            "Instrument Code": "int32",
            "Holder Name": "string",
            "Holder Code": "int16",
            "Issuer Name": "string",
            "Issuer Code": "int16",
            "Date": "string",
            "Level": "float64",
        },
    )
    if data.isna().any().any():
        raise ValueError("FWTW data contain missing values")
    if data.duplicated(_FWTW_KEY).any():
        raise ValueError("FWTW instrument-holder-issuer-date key is not unique")
    if not data["Date"].str.fullmatch(r"\d{4}Q[1-4]").all():
        raise ValueError("FWTW Date must use YYYYQ# format")

    _validate_code_name_mapping(data, "Holder")
    _validate_code_name_mapping(data, "Issuer")
    _validate_code_name_mapping(data, "Instrument")
    return data


def read_fred_national_income(path: str | Path) -> pd.DataFrame:
    """Read annual BEA national income downloaded through FRED.

    Parameters
    ----------
    path
        FRED CSV for series ``A032RC1A027NBEA``.  Published observations are
        annual flows in billions of current dollars.

    Returns
    -------
    pandas.DataFrame
        Columns ``year`` and ``national_income_millions``.  The latter is
        converted to millions of current dollars to match FWTW levels.
    """

    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"national-income file not found: {source}")

    value_column = "A032RC1A027NBEA"
    data = pd.read_csv(source, usecols=["observation_date", value_column])
    dates = pd.to_datetime(data["observation_date"], errors="raise")
    values = pd.to_numeric(data[value_column], errors="raise")
    result = pd.DataFrame(
        {
            "year": dates.dt.year.astype(int),
            "national_income_millions": values * 1_000.0,
        }
    )
    if result["year"].duplicated().any():
        raise ValueError("national income must have one observation per year")
    if not result["national_income_millions"].gt(0.0).all():
        raise ValueError("national income must be strictly positive")
    return result


def build_figure1_series(
    fwtw: pd.DataFrame,
    national_income: pd.DataFrame,
    *,
    start_year: int = 1963,
    end_year: int = 2019,
    definition: Figure1Definition = Figure1Definition(),
) -> pd.DataFrame:
    r"""Construct the level and share series plotted in paper Figure 1.

    Parameters
    ----------
    fwtw
        Validated FWTW data from :func:`read_fwtw`.  ``Level`` is a stock in
        millions of current dollars.
    national_income
        One row per year with ``year`` and ``national_income_millions``.
    start_year, end_year
        Inclusive annual sample.  Year-end (Q4) balance-sheet stocks are used.
    definition
        Federal Reserve sector codes defining households and intermediaries.

    Returns
    -------
    pandas.DataFrame
        One row per year with dollar stocks, ``indirect_share`` as a fraction,
        and ``indirect_assets_to_national_income`` as a ratio.

    Notes
    -----
    Let :math:`D_t(i,H)` be the dollar value of issuer ``i``'s liabilities
    held by households.  The amount behind the intermediation veil is

    .. math::

       V_t = \sum_{i \in \mathcal F} D_t(i,H),

    where :math:`\mathcal F` is the set of financial intermediaries.  Figure 1
    reports :math:`V_t / \sum_{i \ne ROW}D_t(i,H)` and :math:`V_t/NI_t`.
    """

    if start_year > end_year:
        raise ValueError("start_year must not exceed end_year")

    year_end = fwtw.loc[fwtw["Date"].str.endswith("Q4")].copy()
    year_end["year"] = year_end["Date"].str[:4].astype(int)
    year_end = year_end.loc[year_end["year"].between(start_year, end_year)]
    household_assets = year_end.loc[
        (year_end["Holder Code"] == definition.household)
        & ~year_end["Issuer Code"].isin(
            [definition.total_sector, definition.discrepancy_sector]
        )
    ]

    by_issuer = (
        household_assets.groupby(["year", "Issuer Code"], as_index=False)["Level"]
        .sum()
        .rename(columns={"Level": "household_assets_millions"})
    )
    domestic = (
        by_issuer.loc[by_issuer["Issuer Code"] != definition.rest_of_world]
        .groupby("year", as_index=False)["household_assets_millions"]
        .sum()
        .rename(
            columns={
                "household_assets_millions": "us_financial_assets_millions"
            }
        )
    )
    indirect = (
        by_issuer.loc[
            ~by_issuer["Issuer Code"].isin(definition.nonintermediary_issuers)
        ]
        .groupby("year", as_index=False)["household_assets_millions"]
        .sum()
        .rename(
            columns={
                "household_assets_millions": "indirect_household_assets_millions"
            }
        )
    )

    series = domestic.merge(indirect, on="year", how="outer", validate="one_to_one")
    series = series.merge(
        national_income,
        on="year",
        how="left",
        validate="one_to_one",
        indicator=True,
    )
    missing_years = sorted(
        set(range(start_year, end_year + 1)).difference(series["year"])
    )
    if missing_years:
        raise ValueError(f"FWTW sample is missing years: {missing_years}")
    if not series["_merge"].eq("both").all():
        missing_income = series.loc[series["_merge"] != "both", "year"].tolist()
        raise ValueError(f"national income is missing years: {missing_income}")
    series = series.drop(columns="_merge").sort_values("year").reset_index(drop=True)

    if not series["indirect_household_assets_millions"].between(
        0.0, series["us_financial_assets_millions"]
    ).all():
        raise ValueError("indirect household assets must lie within the U.S. total")

    series["indirect_share"] = (
        series["indirect_household_assets_millions"]
        / series["us_financial_assets_millions"]
    )
    series["indirect_assets_to_national_income"] = (
        series["indirect_household_assets_millions"]
        / series["national_income_millions"]
    )
    return series[
        [
            "year",
            "indirect_household_assets_millions",
            "us_financial_assets_millions",
            "national_income_millions",
            "indirect_share",
            "indirect_assets_to_national_income",
        ]
    ]


def plot_figure1(series: pd.DataFrame, output_path: str | Path) -> None:
    """Plot the newer-public-data robustness series and save it to disk."""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    figure, level_axis = plt.subplots(figsize=(9.2, 5.2))
    share_axis = level_axis.twinx()
    level_axis.plot(
        series["year"],
        series["indirect_assets_to_national_income"],
        color="#4E9ACD",
        linewidth=2.5,
        label="Level owned indirectly",
    )
    share_axis.plot(
        series["year"],
        series["indirect_share"],
        color="#8D99A8",
        linewidth=2.5,
        label="Share owned indirectly",
    )
    level_axis.set(
        xlabel="Year",
        ylabel="Indirect household ownership\n(as ratio to national income)",
        title=(
            "Public-data robustness: indirect household ownership "
            "of U.S. financial assets"
        ),
    )
    share_axis.set_ylabel("Share of U.S. financial assets owned indirectly")
    level_axis.grid(axis="both", color="#DCE3E8", linewidth=0.8, alpha=0.8)
    level_axis.spines[["top", "right"]].set_visible(False)
    share_axis.spines["top"].set_visible(False)

    lines = level_axis.lines + share_axis.lines
    level_axis.legend(lines, [line.get_label() for line in lines], loc="upper left")
    figure.tight_layout()
    figure.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(figure)


def _validate_code_name_mapping(data: pd.DataFrame, kind: str) -> None:
    """Require every published code to map to exactly one name."""

    code = f"{kind} Code"
    name = f"{kind} Name"
    mapping = data[[code, name]].drop_duplicates()
    if mapping[code].duplicated().any():
        raise ValueError(f"each {kind.lower()} code must map to one name")
