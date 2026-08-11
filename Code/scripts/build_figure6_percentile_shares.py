"""Rebuild the July 2025 Figure 6 percentile bins from raw DINA data.

The supplied microfile is 16 GB, so the script selects only the required
columns and collapses them in bounded chunks. It never modifies the authors'
file. The generated long share table is the upstream input to
``build_figure6_authors_data.py``.
"""

from __future__ import annotations

from pathlib import Path

from unveiling.figure6_authors import (
    build_percentile_shares,
    validate_against_prepared_fine_shares,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DINA = (
    PROJECT_ROOT
    / "MSS2021Febreplicationkit"
    / "data"
    / "PSZusdina"
    / "usdina19622016.dta"
)
OUTPUT = PROJECT_ROOT / "Data" / "interim" / "figure6_percentile_shares.csv"
VALIDATION_OUTPUT = (
    PROJECT_ROOT / "Data" / "interim" / "figure6_percentile_share_validation.csv"
)
PREPARED_FINE = (
    PROJECT_ROOT
    / "MSS2021Febreplicationkit"
    / "data"
    / "PSZusdina"
    / "Yszshares_fine.dta"
)


def main() -> None:
    """Build and write the validated year-percentile share table."""

    shares = build_percentile_shares(
        RAW_DINA,
        chunksize=1_000_000,
        progress=lambda rows: print(f"Processed {rows:,} raw DINA rows", flush=True),
    )
    validation = validate_against_prepared_fine_shares(shares, PREPARED_FINE)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shares.to_csv(OUTPUT, index=False)
    validation.to_csv(VALIDATION_OUTPUT, index=False)
    print(f"Wrote {OUTPUT.relative_to(PROJECT_ROOT)} ({len(shares):,} rows)")
    print(
        "Prepared-share validation: max absolute error="
        f"{validation['max_absolute_error'].max():.3g}"
    )
    print(f"Wrote {VALIDATION_OUTPUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
