"""Tests for the financial-network unveiling identities."""

import numpy as np
import pytest

from unveiling import DirectOwnershipNetwork


@pytest.fixture
def toy_network() -> DirectOwnershipNetwork:
    """Return a two-owner, two-intermediary cross-holding network."""

    direct_ownership = np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.2, 0.1, 0.0, 0.7],
            [0.6, 0.2, 0.2, 0.0],
        ]
    )
    return DirectOwnershipNetwork(direct_ownership, n_owners=2)


def test_unveiling_matches_paper_equation(toy_network: DirectOwnershipNetwork) -> None:
    """The block solve must equal M(I-M)^-1 from Equation (1)."""

    intermediation = toy_network.intermediation_matrix()
    identity = np.eye(intermediation.shape[0])
    equation_one = intermediation @ np.linalg.inv(identity - intermediation)

    np.testing.assert_allclose(
        toy_network.unveiled_ownership(),
        equation_one[2:, :2],
    )


def test_unveiling_matches_long_round_by_round_sum(
    toy_network: DirectOwnershipNetwork,
) -> None:
    """The closed form must equal many successive intermediation rounds."""

    intermediation = toy_network.intermediation_matrix()
    term = intermediation.copy()
    round_sum = np.zeros_like(intermediation)
    for _ in range(80):
        round_sum += term
        term = term @ intermediation

    np.testing.assert_allclose(
        toy_network.unveiled_ownership(),
        round_sum[2:, :2],
        atol=1e-12,
    )


def test_unveiled_owner_shares_sum_to_one(
    toy_network: DirectOwnershipNetwork,
) -> None:
    """Every intermediary must be fully allocated to ultimate owners."""

    np.testing.assert_allclose(toy_network.unveiled_ownership().sum(axis=1), 1.0)


def test_unveiled_shares_satisfy_network_fixed_point(
    toy_network: DirectOwnershipNetwork,
) -> None:
    """Each ultimate share must equal its direct and indirect connections."""

    omega = toy_network.unveiled_ownership()
    b_matrix = toy_network.direct_ownership[2:, :2]
    q_matrix = toy_network.direct_ownership[2:, 2:]

    np.testing.assert_allclose(omega, b_matrix + q_matrix @ omega)


def test_instrument_constructor_implements_row_scaling() -> None:
    """Equation (4) must aggregate dollars and scale issuer rows."""

    instrument_one = np.diag([60.0, 50.0, 20.0])
    instrument_two = np.array(
        [
            [40.0, 0.0, 0.0],
            [0.0, 50.0, 0.0],
            [40.0, 40.0, 0.0],
        ]
    )
    network = DirectOwnershipNetwork.from_instrument_holdings(
        [instrument_one, instrument_two],
        total_liabilities=[100.0, 100.0, 100.0],
        n_owners=2,
    )

    expected = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.4, 0.4, 0.2],
        ]
    )
    np.testing.assert_allclose(network.direct_ownership, expected)


def test_primary_asset_mapping_preserves_asset_rows(
    toy_network: DirectOwnershipNetwork,
) -> None:
    """Equation (3) must allocate each primary asset completely to owners."""

    p_matrix = np.array([[0.5, 0.3], [0.0, 0.6]])
    lambda_matrix = np.array([[0.1, 0.1], [0.1, 0.3]])

    final_ownership = toy_network.primary_asset_ownership(
        p_matrix,
        lambda_matrix,
    )

    np.testing.assert_allclose(final_ownership.sum(axis=1), 1.0)


def test_net_worth_sums_to_zero(toy_network: DirectOwnershipNetwork) -> None:
    """Equation (2) preserves the closed-system balance-sheet identity."""

    net_worth = toy_network.net_worth([100.0, 80.0, 120.0, 60.0])

    assert net_worth.sum() == pytest.approx(0.0)


def test_nonabsorbing_intermediary_network_fails() -> None:
    """A closed intermediary cycle has no finite ultimate-owner allocation."""

    direct_ownership = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
        ]
    )

    with pytest.raises(ValueError, match="do not converge"):
        DirectOwnershipNetwork(direct_ownership, n_owners=1)
