"""Digitized benchmarks for Figures 5, 6, and 8 of the July 2025 paper.

The values produced here are approximate visual benchmarks. They are never
used as inputs to the empirical reconstruction. Fixed pixel calibrations apply
only to the raster images embedded in ``MSS_SGR_July242025.pdf``.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from matplotlib import image as mpl_image
import numpy as np
import pandas as pd


PAPER_COLORS = {
    "top_1": np.array([200, 82, 0], dtype=np.uint8),
    "next_9": np.array([255, 188, 121], dtype=np.uint8),
    "next_40": np.array([200, 208, 217], dtype=np.uint8),
    "bottom_50": np.array([163, 204, 233], dtype=np.uint8),
    "bottom_99": np.array([17, 112, 170], dtype=np.uint8),
}

FIGURE6_COLORS = {
    "pre_1982": np.array([200, 82, 0], dtype=np.uint8),
    "post_1982": np.array([95, 162, 206], dtype=np.uint8),
}

FIGURE6_PERCENTILES = np.arange(40, 101, dtype=np.int16)
FIGURE6_X_PIXEL_LEFT = 125
FIGURE6_X_PIXEL_RIGHT = 1006
FIGURE6_Y_PIXEL_AT_ZERO = 504.0
FIGURE6_Y_PIXELS_PER_RATE_UNIT = 775.0


def extract_embedded_figure(
    pdf_path: Path,
    output_dir: Path,
    *,
    physical_page: int,
    prefix_name: str,
) -> Path:
    """Extract the single raster embedded on one physical PDF page."""

    prefix = output_dir / prefix_name
    subprocess.run(
        [
            "pdfimages",
            "-f",
            str(physical_page),
            "-l",
            str(physical_page),
            "-png",
            str(pdf_path),
            str(prefix),
        ],
        check=True,
    )
    candidates = sorted(output_dir.glob(f"{prefix_name}-*.png"))
    if len(candidates) != 1:
        raise ValueError(
            f"Expected one {prefix_name} image, found {len(candidates)}"
        )
    return candidates[0]


def _load_rgb(image_path: Path) -> np.ndarray:
    """Load an embedded figure image as eight-bit RGB."""

    image = mpl_image.imread(image_path)
    if np.issubdtype(image.dtype, np.floating):
        image = np.rint(image[..., :3] * 255).astype(np.uint8)
    else:
        image = image[..., :3].astype(np.uint8)
    if image.shape != (698, 1047, 3):
        raise ValueError(f"Unexpected embedded image shape {image.shape}")
    return image


def _trace_exact_color(
    image: np.ndarray,
    *,
    color: np.ndarray,
    years: np.ndarray,
    x_year_left: int,
    x_pixel_left: int,
    x_year_right: int,
    x_pixel_right: int,
    minimum_row: int,
    maximum_row: int,
    early_minimum_row: int | None = None,
    early_cutoff_year: int | None = None,
) -> np.ndarray:
    """Trace a paper line by exact raster color and interpolate dashed gaps."""

    mask = np.all(image == color, axis=2)
    rows_by_year: list[float] = []
    for year in years:
        calendar_year = int(year)
        x = x_pixel_left + (calendar_year - x_year_left) * (
            x_pixel_right - x_pixel_left
        ) / (x_year_right - x_year_left)
        center = round(float(x))
        rows, _ = np.where(mask[:, center - 5 : center + 6])
        floor = minimum_row
        if (
            early_minimum_row is not None
            and early_cutoff_year is not None
            and calendar_year < early_cutoff_year
        ):
            floor = early_minimum_row
        rows = rows[(rows > floor) & (rows < maximum_row)]
        rows_by_year.append(float(np.median(rows)) if len(rows) else np.nan)

    traced = pd.Series(rows_by_year, index=years, dtype=np.float64)
    traced = traced.interpolate(limit_direction="both")
    if traced.isna().any():
        raise ValueError("Paper digitization left unresolved annual gaps")
    return traced.to_numpy()


def digitize_figure5(image_path: Path) -> pd.DataFrame:
    """Digitize all five series in the paper's Figure 5 raster."""

    image = _load_rgb(image_path)
    years = np.arange(1972, 2020, dtype=np.int16)
    output = pd.DataFrame({"year": years})
    for group, color in PAPER_COLORS.items():
        pixels = _trace_exact_color(
            image,
            color=color,
            years=years,
            x_year_left=1970,
            x_pixel_left=163,
            x_year_right=2020,
            x_pixel_right=1006,
            minimum_row=20,
            maximum_row=570,
        )
        column = f"paper_{group}_relative_to_1982"
        output[column] = (245.0 - pixels) / 2565.0
        output[column] -= output.loc[output["year"] == 1982, column].iloc[0]
    return output


def digitize_figure8(image_path: Path) -> pd.DataFrame:
    """Digitize all five series in the paper's Figure 8 raster."""

    image = _load_rgb(image_path)
    years = np.arange(1963, 2020, dtype=np.int16)
    output = pd.DataFrame({"year": years})
    for group, color in PAPER_COLORS.items():
        if group == "top_1":
            early_floor, cutoff = 100, 1990
        else:
            early_floor, cutoff = 100, 2021
        pixels = _trace_exact_color(
            image,
            color=color,
            years=years,
            x_year_left=1960,
            x_pixel_left=163,
            x_year_right=2020,
            x_pixel_right=1006,
            minimum_row=20,
            maximum_row=600,
            early_minimum_row=early_floor,
            early_cutoff_year=cutoff,
        )
        column = f"paper_{group}_relative_to_1982"
        output[column] = (227.0 - pixels) / 885.0
        output[column] -= output.loc[output["year"] == 1982, column].iloc[0]
    return output


def digitize_figure6_coordinates(image_path: Path) -> pd.DataFrame:
    """Recover Figure 6 curve centerlines in the embedded raster.

    Parameters
    ----------
    image_path
        PNG extracted directly from physical page 24 of the July 2025 paper.

    Returns
    -------
    pandas.DataFrame
        One row per period and integer wealth percentile. ``x_pixel`` and
        ``y_pixel`` are coordinates in the 1047-by-698 embedded raster;
        ``matched_exact_pixels`` counts curve-color pixels in the eleven-pixel
        horizontal sampling strip; and ``was_interpolated`` records whether a
        dashed-line gap required interpolation between neighboring samples.
    """

    image = _load_rgb(image_path)
    records: list[dict[str, float | int | bool | str]] = []
    for period, color in FIGURE6_COLORS.items():
        mask = np.all(image == color, axis=2)
        for percentile in FIGURE6_PERCENTILES:
            x = FIGURE6_X_PIXEL_LEFT + (int(percentile) - 40) * (
                FIGURE6_X_PIXEL_RIGHT - FIGURE6_X_PIXEL_LEFT
            ) / 60
            center = round(float(x))
            rows, _ = np.where(mask[:, center - 5 : center + 6])
            if percentile <= 45:
                minimum_row = 400
            elif percentile <= 70:
                minimum_row = 300
            elif percentile <= 90:
                minimum_row = 175
            else:
                minimum_row = 30
            rows = rows[(rows > minimum_row) & (rows < 590)]
            y_pixel = float(np.median(rows)) if len(rows) else np.nan
            sampling_rule = "median_exact_color_strip"
            if percentile == 100 and len(rows):
                endpoint_block = mask[:, center - 10 : center + 11]
                row_widths = endpoint_block.sum(axis=1)
                row_widths[: minimum_row + 1] = 0
                row_widths[590:] = 0
                maximum_width = row_widths.max()
                widest_rows = np.flatnonzero(row_widths == maximum_width)
                y_pixel = float(np.median(widest_rows))
                sampling_rule = "endpoint_marker_center"
            records.append(
                {
                    "period": period,
                    "wealth_percentile": int(percentile),
                    "x_pixel": float(x),
                    "sample_column": center,
                    "y_pixel": y_pixel,
                    "matched_exact_pixels": int(len(rows)),
                    "was_interpolated": len(rows) == 0,
                    "sampling_rule": sampling_rule,
                }
            )

    coordinates = pd.DataFrame.from_records(records)
    coordinates["y_pixel"] = coordinates.groupby(
        "period", sort=False
    )["y_pixel"].transform(
        lambda series: series.interpolate(limit_direction="both")
    )
    if coordinates["y_pixel"].isna().any():
        missing_periods = coordinates.loc[
            coordinates["y_pixel"].isna(), "period"
        ].unique()
        raise ValueError(
            "Figure 6 digitization left unresolved gaps for "
            f"{missing_periods.tolist()}"
        )
    coordinates["saving_rate"] = (
        FIGURE6_Y_PIXEL_AT_ZERO - coordinates["y_pixel"]
    ) / FIGURE6_Y_PIXELS_PER_RATE_UNIT
    return coordinates


def digitize_figure6(image_path: Path) -> pd.DataFrame:
    """Digitize the two saving-rate curves in the paper's Figure 6 raster."""

    coordinates = digitize_figure6_coordinates(image_path)
    output = pd.DataFrame({"wealth_percentile": FIGURE6_PERCENTILES})
    for period in FIGURE6_COLORS:
        traced = coordinates.loc[
            coordinates["period"] == period,
            ["wealth_percentile", "saving_rate"],
        ]
        if len(traced) != len(FIGURE6_PERCENTILES):
            raise ValueError(
                f"Figure 6 digitization has incomplete {period} coordinates"
            )
        output = output.merge(
            traced.rename(columns={"saving_rate": f"paper_{period}_rate"}),
            on="wealth_percentile",
            how="left",
            validate="one_to_one",
        )
    return output
