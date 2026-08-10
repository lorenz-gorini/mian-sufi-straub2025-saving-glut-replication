"""Financial-network unveiling following Mian, Straub, and Sufi (2025)."""

from .network import DirectOwnershipNetwork


_FIGURE1_EXPORTS = {
    "Figure1Definition",
    "build_figure1_series",
    "plot_figure1",
    "read_fred_national_income",
    "read_fwtw",
}


def __getattr__(name: str):
    """Load the public-data Figure 1 helpers only when they are requested."""

    if name in _FIGURE1_EXPORTS:
        from . import figure1

        return getattr(figure1, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "DirectOwnershipNetwork",
    "Figure1Definition",
    "build_figure1_series",
    "plot_figure1",
    "read_fred_national_income",
    "read_fwtw",
]
