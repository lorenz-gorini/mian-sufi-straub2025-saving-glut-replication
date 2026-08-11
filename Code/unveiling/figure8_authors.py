"""Construct the best-feasible Figure 8 proxy from the 2021 author kit.

The supplied file contains fine-cohort household-debt assets after the old
seven-round unveiling and fine-cohort debt liabilities.  The module applies
the July 2025 net-debt definition and 1982 normalization, but it does not claim
to reproduce the unavailable 2025 augmented-matrix solve.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .wealth_groups import FINE_COHORTS, WEALTH_GROUP_COHORTS


GROUPS = tuple(WEALTH_GROUP_COHORTS)


def load_fine_debt_positions(path: Path) -> pd.DataFrame:
    """Load fine-cohort old-unveiling assets, liabilities, and national income.

    Monetary values are current-dollar millions. Debt liabilities are stored
    as positive stocks in this supplied file and are subtracted from assets.
    """

    columns = [
        "year",
        "fa896140001a",
        *(
            f"{side}_hh{cohort}_hhdSZ"
            for side in ("a", "d")
            for cohort in FINE_COHORTS
        ),
        "a_hh1_hhdSZ",
        "d_hh1_hhdSZ",
        "a_hh9_hhdSZ",
        "d_hh9_hhdSZ",
        "a_hh90_hhdSZ",
        "d_hh90_hhdSZ",
    ]
    frame = pd.read_stata(path, columns=columns, convert_categoricals=False)
    years = pd.to_numeric(frame["year"], errors="raise")
    if years.isna().any() or not np.allclose(years, np.rint(years)):
        raise ValueError("fine debt positions: year must contain finite integers")
    frame["year"] = np.rint(years).astype(np.int16)
    frame = frame.loc[frame["year"].between(1963, 2016)].copy()
    frame[columns[1:]] = frame[columns[1:]].astype(np.float64)
    if frame["year"].duplicated().any():
        raise ValueError("fine debt positions: duplicate annual keys")
    if not np.isfinite(frame.to_numpy(dtype=float)).all():
        raise ValueError("fine debt positions: required values must be finite")
    if (frame["fa896140001a"] <= 0).any():
        raise ValueError("fine debt positions: national income must be positive")
    return frame.sort_values("year").reset_index(drop=True)


def construct_figure8_proxy(
    fine_positions: pd.DataFrame,
    *,
    base_year: int = 1982,
    aggregation_tolerance: float = 2e-6,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Aggregate cohorts and apply ``ND = debt assets - debt liabilities``.

    Returns
    -------
    result, validation : tuple[pandas.DataFrame, pandas.DataFrame]
        ``result`` has one annual row and the five paper display series.
        ``validation`` compares fine-cohort sums with the supplied top-1,
        next-9, and bottom-90 cells.
    """

    frame = fine_positions.copy()
    output = frame[["year"]].copy()
    output["national_income_millions"] = frame["fa896140001a"]
    for group, cohorts in WEALTH_GROUP_COHORTS.items():
        asset_columns = [f"a_hh{cohort}_hhdSZ" for cohort in cohorts]
        liability_columns = [f"d_hh{cohort}_hhdSZ" for cohort in cohorts]
        output[f"debt_assets_{group}_millions"] = frame[asset_columns].sum(
            axis=1
        )
        output[f"debt_liabilities_{group}_millions"] = frame[
            liability_columns
        ].sum(axis=1)
        output[f"net_debt_{group}_millions"] = (
            output[f"debt_assets_{group}_millions"]
            - output[f"debt_liabilities_{group}_millions"]
        )
        ratio = (
            output[f"net_debt_{group}_millions"]
            / output["national_income_millions"]
        )
        base = ratio.loc[output["year"] == base_year]
        if len(base) != 1:
            raise ValueError(f"Figure 8 proxy: missing unique {base_year} base")
        output[f"net_debt_{group}_relative_to_{base_year}"] = (
            ratio - base.iloc[0]
        )

    for measure in ("debt_assets", "debt_liabilities", "net_debt"):
        output[f"{measure}_bottom_99_millions"] = sum(
            output[f"{measure}_{group}_millions"]
            for group in ("next_9", "next_40", "bottom_50")
        )
    bottom_99_ratio = (
        output["net_debt_bottom_99_millions"]
        / output["national_income_millions"]
    )
    bottom_99_base = bottom_99_ratio.loc[output["year"] == base_year].iloc[0]
    output[f"net_debt_bottom_99_relative_to_{base_year}"] = (
        bottom_99_ratio - bottom_99_base
    )

    validation_records = []
    coarse_groups = {
        "top_1": ("top_1", "1"),
        "next_9": ("next_9", "9"),
        "bottom_90": (("next_40", "bottom_50"), "90"),
    }
    for label, (components, suffix) in coarse_groups.items():
        groups = (components,) if isinstance(components, str) else components
        for side, measure in (("a", "debt_assets"), ("d", "debt_liabilities")):
            reconstructed = sum(
                output[f"{measure}_{group}_millions"] for group in groups
            )
            benchmark = frame[f"{side}_hh{suffix}_hhdSZ"]
            record = pd.DataFrame(
                {
                    "year": frame["year"],
                    "group": label,
                    "side": "asset" if side == "a" else "liability",
                    "fine_sum_millions": reconstructed,
                    "coarse_benchmark_millions": benchmark,
                }
            )
            record["error_millions"] = (
                record["fine_sum_millions"]
                - record["coarse_benchmark_millions"]
            )
            record["relative_error"] = record["error_millions"] / record[
                "coarse_benchmark_millions"
            ].abs().clip(lower=1.0)
            validation_records.append(record)
    validation = pd.concat(validation_records, ignore_index=True)
    if validation["relative_error"].abs().max() > aggregation_tolerance:
        raise ValueError("Figure 8 proxy: fine-to-coarse aggregation failed")

    output = output.loc[output["year"].between(1963, 2016)].reset_index(drop=True)
    if output["year"].tolist() != list(range(1963, 2017)):
        raise ValueError("Figure 8 proxy: expected complete 1963-2016 sample")
    return output, validation.loc[
        validation["year"].between(1963, 2016)
    ].reset_index(drop=True)
