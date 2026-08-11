"""Tests for paper-raster digitization helpers."""

from pathlib import Path

from matplotlib import image as mpl_image
import numpy as np

from unveiling.paper_benchmarks import (
    FIGURE6_COLORS,
    FIGURE6_PERCENTILES,
    FIGURE6_X_PIXEL_LEFT,
    FIGURE6_X_PIXEL_RIGHT,
    FIGURE6_Y_PIXEL_AT_ZERO,
    FIGURE6_Y_PIXELS_PER_RATE_UNIT,
    digitize_figure6,
    digitize_figure6_coordinates,
)


def _write_synthetic_figure6(path: Path) -> None:
    """Write an exact-color Figure 6 raster with one deliberate dash gap."""

    image = np.full((698, 1047, 3), 255, dtype=np.uint8)
    rates = {"pre_1982": 0.05, "post_1982": -0.02}
    for period, color in FIGURE6_COLORS.items():
        row = round(
            FIGURE6_Y_PIXEL_AT_ZERO
            - rates[period] * FIGURE6_Y_PIXELS_PER_RATE_UNIT
        )
        for percentile in FIGURE6_PERCENTILES:
            if period == "post_1982" and percentile == 70:
                continue
            column = round(
                FIGURE6_X_PIXEL_LEFT
                + (int(percentile) - 40)
                * (FIGURE6_X_PIXEL_RIGHT - FIGURE6_X_PIXEL_LEFT)
                / 60
            )
            image[row - 1 : row + 2, column - 1 : column + 2] = color
    mpl_image.imsave(path, image)


def test_figure6_digitization_records_and_interpolates_pixels(
    tmp_path: Path,
) -> None:
    """Exact-color samples are retained and a missing dash is explicit."""

    image_path = tmp_path / "figure6.png"
    _write_synthetic_figure6(image_path)

    coordinates = digitize_figure6_coordinates(image_path)
    rates = digitize_figure6(image_path)

    assert len(coordinates) == 2 * len(FIGURE6_PERCENTILES)
    missing = coordinates.loc[coordinates["was_interpolated"]]
    assert missing[["period", "wealth_percentile"]].to_dict("records") == [
        {"period": "post_1982", "wealth_percentile": 70}
    ]
    assert np.isfinite(coordinates["y_pixel"]).all()
    assert np.allclose(rates["paper_pre_1982_rate"], 0.05, atol=0.001)
    assert np.allclose(rates["paper_post_1982_rate"], -0.02, atol=0.001)
