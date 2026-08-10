"""Leontief-style unveiling of financial intermediary cross-holdings.

Rows are liability issuers (borrowers) and columns are direct holders
(lenders), exactly as in Sections 2.1--2.2 of Mian, Straub, and Sufi (2025).
Ultimate owners occupy the first ``n_owners`` rows and columns.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatArray = NDArray[np.float64]
_TOLERANCE = 1e-10


@dataclass(frozen=True, slots=True)
class DirectOwnershipNetwork:
    r"""A validated direct ownership matrix, :math:`\bar M_t`.

    Parameters
    ----------
    direct_ownership
        Square matrix whose entry ``[i, j]`` is the share of liabilities
        issued by sector ``i`` and held directly by sector ``j``. Rows must
        sum to one. Shares are unit-free fractions, not percentages.
    n_owners
        Number of ultimate owners. They must occupy the first rows and columns
        of ``direct_ownership``; the remaining sectors are intermediaries.

    Raises
    ------
    ValueError
        If the matrix is structurally invalid or intermediary chains do not
        converge to ultimate owners.
    """

    direct_ownership: FloatArray
    n_owners: int

    def __post_init__(self) -> None:
        matrix = np.array(self.direct_ownership, dtype=float, copy=True)
        _validate_direct_ownership(matrix, self.n_owners)
        matrix.setflags(write=False)
        object.__setattr__(self, "direct_ownership", matrix)

    @classmethod
    def from_instrument_holdings(
        cls,
        instrument_holdings: ArrayLike,
        total_liabilities: ArrayLike,
        n_owners: int,
    ) -> DirectOwnershipNetwork:
        r"""Construct :math:`\bar M_t` from instrument-level dollar holdings.

        This implements Equation (4): sum the completed from-whom-to-whom
        matrices over instruments, then divide each issuer row by that
        issuer's total liabilities.

        Parameters
        ----------
        instrument_holdings
            Array with shape ``(n_instruments, n_sectors, n_sectors)`` in
            dollars. Entry ``[h, i, j]`` is instrument ``h`` issued by sector
            ``i`` and held by sector ``j``.
        total_liabilities
            Length-``n_sectors`` vector of issuer liabilities in dollars.
        n_owners
            Number of ultimate owners, ordered first.

        Returns
        -------
        DirectOwnershipNetwork
            Network expressed in liability shares.

        Notes
        -----
        Missing-cell estimation is upstream of this constructor. The input
        instrument matrices must already be complete, as required before the
        paper applies Equation (4).
        """

        holdings = np.asarray(instrument_holdings, dtype=float)
        liabilities = np.asarray(total_liabilities, dtype=float)
        _validate_instrument_inputs(holdings, liabilities)

        direct_ownership = holdings.sum(axis=0) / liabilities[:, None]
        return cls(direct_ownership, n_owners)

    @property
    def n_intermediaries(self) -> int:
        """Return the number of intermediary sectors, :math:`k`."""

        return self.direct_ownership.shape[0] - self.n_owners

    def intermediation_matrix(self) -> FloatArray:
        """Return :math:`M_t`, obtained by zeroing the ultimate-owner rows."""

        matrix = self.direct_ownership.copy()
        matrix[: self.n_owners, :] = 0.0
        return matrix

    def unveiled_ownership(self) -> FloatArray:
        r"""Compute the unveiled intermediary-to-owner matrix :math:`\Omega_t`.

        Returns
        -------
        numpy.ndarray
            A ``(k, m)`` matrix. Entry ``[i, j]`` is the share of intermediary
            ``i`` ultimately owned by owner ``j``, directly and through every
            possible chain of intermediary cross-holdings.

        Notes
        -----
        Equation (1) is

        .. math::

           \bar\Omega_t = M_t + M_t^2 + \cdots = M_t(I-M_t)^{-1}.

        With owners ordered first, write the nonzero block of ``M_t`` as
        ``[B, Q]``, where ``B`` contains direct owner holdings and ``Q``
        intermediary cross-holdings. The desired submatrix is equivalently
        ``Omega = (I - Q)^{-1} B``. ``numpy.linalg.solve`` computes this system
        without forming an explicit inverse.
        """

        owner_holdings = self.direct_ownership[
            self.n_owners :, : self.n_owners
        ]
        cross_holdings = self.direct_ownership[
            self.n_owners :, self.n_owners :
        ]
        identity = np.eye(self.n_intermediaries)

        return np.linalg.solve(identity - cross_holdings, owner_holdings)

    def net_worth(self, total_liabilities: ArrayLike) -> FloatArray:
        """Map direct ownership into sector net worth using Equation (2).

        Parameters
        ----------
        total_liabilities
            Length-``(m + k)`` row vector of total liabilities in dollars.

        Returns
        -------
        numpy.ndarray
            Sector net worth in dollars: ``L @ direct_ownership - L``.
        """

        liabilities = np.asarray(total_liabilities, dtype=float)
        _validate_liability_vector(liabilities, self.direct_ownership.shape[0])
        return liabilities @ self.direct_ownership - liabilities

    def primary_asset_ownership(
        self,
        intermediary_holdings: ArrayLike,
        direct_owner_holdings: ArrayLike,
    ) -> FloatArray:
        r"""Map primary assets to ultimate owners using Equation (3).

        Parameters
        ----------
        intermediary_holdings
            Matrix :math:`P_t` with shape ``(n_assets, k)``. Each entry is a
            primary asset's direct holding share assigned to an intermediary.
        direct_owner_holdings
            Matrix :math:`\Lambda_t` with shape ``(n_assets, m)``. Each entry
            is a primary asset's share held directly by an ultimate owner.

        Returns
        -------
        numpy.ndarray
            Matrix :math:`A_t = P_t\Omega_t + \Lambda_t` with shape
            ``(n_assets, m)``. Rows give final owner shares of each asset.

        Raises
        ------
        ValueError
            If dimensions, shares, or the combined row-sum identity are
            inconsistent.
        """

        p_matrix = np.asarray(intermediary_holdings, dtype=float)
        lambda_matrix = np.asarray(direct_owner_holdings, dtype=float)
        _validate_primary_asset_inputs(
            p_matrix,
            lambda_matrix,
            self.n_intermediaries,
            self.n_owners,
        )
        return p_matrix @ self.unveiled_ownership() + lambda_matrix


def _validate_direct_ownership(matrix: FloatArray, n_owners: int) -> None:
    """Validate the input boundary for a direct ownership network."""

    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("direct_ownership must be a square two-dimensional matrix")
    n_sectors = matrix.shape[0]
    if not 0 < n_owners < n_sectors:
        raise ValueError("n_owners must leave at least one intermediary sector")
    if not np.isfinite(matrix).all():
        raise ValueError("direct_ownership must contain only finite shares")
    if (matrix < -_TOLERANCE).any():
        raise ValueError("direct_ownership cannot contain negative shares")
    if not np.allclose(matrix.sum(axis=1), 1.0, atol=_TOLERANCE, rtol=0.0):
        raise ValueError("each direct_ownership row must sum to one")

    cross_holdings = matrix[n_owners:, n_owners:]
    spectral_radius = np.max(np.abs(np.linalg.eigvals(cross_holdings)))
    if spectral_radius >= 1.0 - _TOLERANCE:
        raise ValueError(
            "intermediary cross-holdings do not converge to ultimate owners"
        )


def _validate_instrument_inputs(
    holdings: FloatArray,
    liabilities: FloatArray,
) -> None:
    """Validate completed instrument matrices before applying Equation (4)."""

    if holdings.ndim != 3 or holdings.shape[1] != holdings.shape[2]:
        raise ValueError(
            "instrument_holdings must have shape "
            "(n_instruments, n_sectors, n_sectors)"
        )
    if not np.isfinite(holdings).all() or (holdings < -_TOLERANCE).any():
        raise ValueError("instrument_holdings must be finite and non-negative")
    _validate_liability_vector(liabilities, holdings.shape[1])
    if (liabilities <= 0.0).any():
        raise ValueError("total_liabilities must be strictly positive")


def _validate_liability_vector(liabilities: FloatArray, n_sectors: int) -> None:
    """Validate a sector-level liability vector."""

    if liabilities.shape != (n_sectors,):
        raise ValueError(f"total_liabilities must have shape ({n_sectors},)")
    if not np.isfinite(liabilities).all():
        raise ValueError("total_liabilities must contain only finite values")


def _validate_primary_asset_inputs(
    p_matrix: FloatArray,
    lambda_matrix: FloatArray,
    n_intermediaries: int,
    n_owners: int,
) -> None:
    """Validate the primary-asset mapping matrices at their input boundary."""

    if p_matrix.ndim != 2 or p_matrix.shape[1] != n_intermediaries:
        raise ValueError(
            f"intermediary_holdings must have {n_intermediaries} columns"
        )
    if lambda_matrix.shape != (p_matrix.shape[0], n_owners):
        raise ValueError(
            "direct_owner_holdings must have the same number of rows as "
            f"intermediary_holdings and {n_owners} columns"
        )
    combined = np.concatenate((lambda_matrix, p_matrix), axis=1)
    if not np.isfinite(combined).all() or (combined < -_TOLERANCE).any():
        raise ValueError("primary-asset holding shares must be finite and non-negative")
    if not np.allclose(combined.sum(axis=1), 1.0, atol=_TOLERANCE, rtol=0.0):
        raise ValueError(
            "direct and intermediary holding shares must sum to one for each asset"
        )
