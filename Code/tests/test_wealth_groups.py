"""Tests for the fine-cohort wealth-group partition."""

from unveiling.wealth_groups import (
    FINE_COHORTS,
    WEALTH_GROUP_COHORTS,
    validate_wealth_group_partition,
)


def test_paper_groups_partition_all_fine_cohorts_once() -> None:
    validate_wealth_group_partition()
    flattened = [
        cohort
        for cohorts in WEALTH_GROUP_COHORTS.values()
        for cohort in cohorts
    ]
    assert len(flattened) == len(FINE_COHORTS)
    assert set(flattened) == set(FINE_COHORTS)
