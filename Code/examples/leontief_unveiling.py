"""Worked numerical example for the paper's unveiling Equation (1).

The example is deliberately small enough to draw as a complete network.  Its
bank--fund cross-holding cycle nevertheless creates ownership paths of
arbitrary length, so the Leontief sum is doing real work.
"""

import numpy as np

from unveiling import DirectOwnershipNetwork


def main() -> None:
    """Unveil a reciprocal bank--fund network into its ultimate owners."""

    # Rows issue liabilities; columns hold them.
    # Sector order: household, government, bank, fund.
    direct_ownership = np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.2, 0.1, 0.0, 0.7],
            [0.6, 0.2, 0.2, 0.0],
        ]
    )
    network = DirectOwnershipNetwork(direct_ownership, n_owners=2)
    unveiled = network.unveiled_ownership()

    print("Sector order: household (H), government (G), bank (B), fund (F)")
    print("Rows issue liabilities; columns hold them.\n")
    print("Direct ownership matrix M_bar:")
    print(direct_ownership)
    print("\nDirect owner shares B:")
    print(direct_ownership[2:, :2])
    print("\nIntermediary cross-holdings Q:")
    print(direct_ownership[2:, 2:])
    print("\nUnveiled owner shares Omega:")
    print(unveiled)

    bank_household = (
        direct_ownership[2, 0] + direct_ownership[2, 3] * unveiled[1, 0]
    )
    fund_household = (
        direct_ownership[3, 0] + direct_ownership[3, 2] * unveiled[0, 0]
    )
    print("\nHousehold ownership fixed point:")
    print(f"  omega_BH = 0.20 + 0.70 * omega_FH = {bank_household:.5f}")
    print(f"  omega_FH = 0.60 + 0.20 * omega_BH = {fund_household:.5f}")

    print("\nBank-to-household contributions by path length:")
    q_matrix = direct_ownership[2:, 2:]
    b_matrix = direct_ownership[2:, :2]
    q_power = np.eye(q_matrix.shape[0])
    for path_length in range(1, 7):
        contribution = (q_power @ b_matrix)[0, 0]
        print(f"  length {path_length}: {contribution:.6f}")
        q_power = q_power @ q_matrix


if __name__ == "__main__":
    main()
