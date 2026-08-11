"""Wealth-group definitions shared by the selected distributional figures."""

from __future__ import annotations


FINE_COHORTS = (
    "f10",
    "f20",
    "f30",
    "f35",
    "f40",
    "f45",
    "f50",
    "f55",
    "f60",
    "f65",
    "f70",
    "f75",
    "f80",
    "f85",
    "f90",
    "f95",
    "f99",
    "f999",
    "f9999",
    "f99999",
    "f00001",
)

# Population mass represented by each cohort.  The labels come from the
# percentile cuts in the authors' ``build_fa_unveiling_data.do`` file.
FINE_COHORT_POPULATION_SHARES = {
    "f10": 0.10,
    "f20": 0.10,
    "f30": 0.10,
    "f35": 0.05,
    "f40": 0.05,
    "f45": 0.05,
    "f50": 0.05,
    "f55": 0.05,
    "f60": 0.05,
    "f65": 0.05,
    "f70": 0.05,
    "f75": 0.05,
    "f80": 0.05,
    "f85": 0.05,
    "f90": 0.05,
    "f95": 0.05,
    "f99": 0.04,
    "f999": 0.009,
    "f9999": 0.0009,
    "f99999": 0.00009,
    "f00001": 0.00001,
}

FINE_COHORT_LABELS = {
    "f10": "Bottom 10%",
    "f20": "10–20%",
    "f30": "20–30%",
    "f35": "30–35%",
    "f40": "35–40%",
    "f45": "40–45%",
    "f50": "45–50%",
    "f55": "50–55%",
    "f60": "55–60%",
    "f65": "60–65%",
    "f70": "65–70%",
    "f75": "70–75%",
    "f80": "75–80%",
    "f85": "80–85%",
    "f90": "85–90%",
    "f95": "90–95%",
    "f99": "95–99%",
    "f999": "99–99.9%",
    "f9999": "99.9–99.99%",
    "f99999": "99.99–99.999%",
    "f00001": "Top 0.001%",
}

TOP_TEN_FINE_COHORTS = (
    "f95",
    "f99",
    "f999",
    "f9999",
    "f99999",
    "f00001",
)

WEALTH_GROUP_COHORTS = {
    "bottom_50": ("f10", "f20", "f30", "f35", "f40", "f45", "f50"),
    "next_40": ("f55", "f60", "f65", "f70", "f75", "f80", "f85", "f90"),
    "next_9": ("f95", "f99"),
    "top_1": ("f999", "f9999", "f99999", "f00001"),
}


def validate_wealth_group_partition() -> None:
    """Require the four paper groups to partition every supplied fine cohort."""

    flattened = tuple(
        cohort
        for cohorts in WEALTH_GROUP_COHORTS.values()
        for cohort in cohorts
    )
    if len(flattened) != len(set(flattened)):
        raise ValueError("wealth groups contain overlapping fine cohorts")
    if set(flattened) != set(FINE_COHORTS):
        missing = sorted(set(FINE_COHORTS) - set(flattened))
        extra = sorted(set(flattened) - set(FINE_COHORTS))
        raise ValueError(
            f"wealth groups do not partition fine cohorts; missing={missing}, "
            f"extra={extra}"
        )
    if set(FINE_COHORT_POPULATION_SHARES) != set(FINE_COHORTS):
        raise ValueError("population shares do not cover every fine cohort")
    if set(FINE_COHORT_LABELS) != set(FINE_COHORTS):
        raise ValueError("labels do not cover every fine cohort")
    population_mass = sum(FINE_COHORT_POPULATION_SHARES.values())
    if abs(population_mass - 1.0) > 1e-12:
        raise ValueError(
            "fine-cohort population shares do not sum to one; "
            f"sum={population_mass:.12g}"
        )


validate_wealth_group_partition()
