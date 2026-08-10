"""Tests for the Figure 1 data definition and input boundaries."""

import pandas as pd
import pytest

from unveiling import (
    build_figure1_series,
    read_fred_national_income,
    read_fwtw,
)


def test_figure1_separates_intermediaries_from_total_financial_assets() -> None:
    """Only financial-intermediary claims belong in the numerator."""

    rows = []
    issuer_levels = {
        15: 10.0,  # Household liabilities: denominator only.
        21: 10.0,  # State/local government: denominator only.
        26: 50.0,  # Rest of world: excluded from both series.
        31: 20.0,  # Federal government: denominator only.
        10: 30.0,  # Corporate business: denominator only.
        11: 10.0,  # Noncorporate business: denominator only.
        65: 20.0,  # Mutual fund: indirect numerator and denominator.
        76: 40.0,  # Bank: indirect numerator and denominator.
    }
    for issuer, level in issuer_levels.items():
        rows.append(
            {
                "Date": "2000Q4",
                "Holder Code": 15,
                "Issuer Code": issuer,
                "Level": level,
            }
        )
    fwtw = pd.DataFrame(rows)
    national_income = pd.DataFrame(
        {"year": [2000], "national_income_millions": [100.0]}
    )

    result = build_figure1_series(
        fwtw,
        national_income,
        start_year=2000,
        end_year=2000,
    ).iloc[0]

    assert result["indirect_household_assets_millions"] == pytest.approx(60.0)
    assert result["us_financial_assets_millions"] == pytest.approx(140.0)
    assert result["indirect_share"] == pytest.approx(60.0 / 140.0)
    assert result["indirect_assets_to_national_income"] == pytest.approx(0.6)


def test_fred_reader_converts_billions_to_millions(tmp_path) -> None:
    """National income must use the same million-dollar unit as FWTW levels."""

    path = tmp_path / "national_income.csv"
    pd.DataFrame(
        {
            "observation_date": ["2000-01-01"],
            "A032RC1A027NBEA": [12_500.0],
        }
    ).to_csv(path, index=False)

    result = read_fred_national_income(path)

    assert result.to_dict("records") == [
        {"year": 2000, "national_income_millions": 12_500_000.0}
    ]


def test_fwtw_reader_rejects_duplicate_primary_key(tmp_path) -> None:
    """An instrument-holder-issuer-quarter relationship must be unique."""

    row = {
        "Instrument Name": "Deposits",
        "Instrument Code": 30300,
        "Holder Name": "Households",
        "Holder Code": 15,
        "Issuer Name": "Bank",
        "Issuer Code": 76,
        "Date": "2000Q4",
        "Level": 10.0,
    }
    path = tmp_path / "fwtw.csv"
    pd.DataFrame([row, row]).to_csv(path, index=False)

    with pytest.raises(ValueError, match="key is not unique"):
        read_fwtw(path)
