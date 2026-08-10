"""Build the authors-data Figure 1 reconstruction and comparison artifacts."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import image as mpl_image
import numpy as np
import pandas as pd

from unveiling.figure1_authors import (
    aggregate_crsp_financial_equity,
    construct_authors_figure1,
    load_author_allocations,
    load_author_balance_sheet,
    load_author_national_income,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUTHOR_DATA = PROJECT_ROOT / "MSS2021Febreplicationkit" / "data"
PAPER_PDF = PROJECT_ROOT / "MSS_SGR_July242025.pdf"

AUTHORS_OUTPUT = (
    PROJECT_ROOT / "Data" / "processed" / "figure1_authors_data.csv"
)
PAPER_OUTPUT = (
    PROJECT_ROOT / "Data" / "processed" / "figure1_paper_digitized.csv"
)
COMPARISON_OUTPUT = (
    PROJECT_ROOT / "Data" / "processed" / "figure1_authors_comparison.csv"
)
FIGURE_OUTPUT = (
    PROJECT_ROOT
    / "Results_Proposal"
    / "figures"
    / "figure1_authors_data_comparison.png"
)
MACRO_OUTPUT = (
    PROJECT_ROOT / "Presentation" / "generated" / "figure1_authors_values.tex"
)


def extract_paper_figure(pdf_path: Path, output_dir: Path) -> Path:
    """Extract the embedded Figure 1 raster from physical PDF page 11."""

    prefix = output_dir / "figure1"
    subprocess.run(
        [
            "pdfimages",
            "-f",
            "11",
            "-l",
            "11",
            "-png",
            str(pdf_path),
            str(prefix),
        ],
        check=True,
    )
    candidates = sorted(output_dir.glob("figure1-*.png"))
    if len(candidates) != 1:
        raise ValueError(
            f"Expected one embedded Figure 1 image, found {len(candidates)}"
        )
    return candidates[0]


def digitize_paper_figure(image_path: Path) -> pd.DataFrame:
    """Digitize both colored annual series from the paper's embedded image.

    Axis and color calibration is fixed to the 807 x 538 image embedded in the
    authoritative July 2025 PDF.  Values are approximate and are used only as
    a visual benchmark, never as an input to the reconstruction.
    """

    image = mpl_image.imread(image_path)
    if np.issubdtype(image.dtype, np.floating):
        image = np.rint(image[..., :3] * 255).astype(np.uint8)
    else:
        image = image[..., :3]
    if image.shape != (538, 807, 3):
        raise ValueError(f"Unexpected Figure 1 image shape {image.shape}")

    x_1960, x_2020 = 121, 706
    blue = np.array([95, 162, 206])
    gray = np.array([163, 172, 185])

    def trace(color: np.ndarray, *, discard_legend: bool) -> np.ndarray:
        mask = np.all(image == color, axis=2)
        values: list[float] = []
        for year in range(1963, 2020):
            x = x_1960 + (year - 1960) * (x_2020 - x_1960) / 60
            x_center = round(x)
            rows, _ = np.where(mask[:, x_center - 2 : x_center + 3])
            rows = rows[(rows > 20) & (rows < 466)]
            if discard_legend and year < 1970:
                rows = rows[rows > 100]
            if len(rows) < 3:
                raise ValueError(f"Could not digitize {year} from {image_path}")
            values.append(float(np.median(rows)))
        return np.asarray(values)

    level_pixels = trace(blue, discard_legend=True)
    share_pixels = trace(gray, discard_legend=True)
    levels = 3.0 - (level_pixels - 31) * 1.5 / (423 - 31)
    shares = 0.70 - (share_pixels - 31) * 0.25 / (453 - 31)
    return pd.DataFrame(
        {
            "year": np.arange(1963, 2020, dtype=np.int16),
            "paper_indirect_assets_to_national_income": levels,
            "paper_indirect_share": shares,
        }
    )


def build_comparison(
    authors: pd.DataFrame, paper: pd.DataFrame
) -> pd.DataFrame:
    """Merge annual reconstructed and digitized series with deviations."""

    comparison = paper.merge(
        authors[
            [
                "year",
                "indirect_assets_to_national_income",
                "indirect_share_proxy",
                "indirect_share_broad",
            ]
        ],
        on="year",
        how="inner",
        validate="one_to_one",
    )
    comparison["level_error"] = (
        comparison["indirect_assets_to_national_income"]
        - comparison["paper_indirect_assets_to_national_income"]
    )
    comparison["share_proxy_error"] = (
        comparison["indirect_share_proxy"]
        - comparison["paper_indirect_share"]
    )
    comparison["share_broad_error"] = (
        comparison["indirect_share_broad"]
        - comparison["paper_indirect_share"]
    )
    return comparison


def plot_comparison(comparison: pd.DataFrame, output_path: Path) -> None:
    """Plot the paper benchmark against the authors-data reconstruction."""

    navy = "#12304A"
    orange = "#D97706"
    gray = "#8A96A3"
    figure, axes = plt.subplots(1, 2, figsize=(10.8, 4.0), sharex=True)

    axes[0].plot(
        comparison["year"],
        comparison["paper_indirect_assets_to_national_income"],
        color=gray,
        linewidth=2.5,
        label="2025 paper (digitized)",
    )
    axes[0].plot(
        comparison["year"],
        comparison["indirect_assets_to_national_income"],
        color=orange,
        linewidth=2.2,
        label="Authors' 2021 data + our equity extension",
    )
    axes[0].set_title("Level behind the veil")
    axes[0].set_ylabel("Ratio to national income")

    axes[1].plot(
        comparison["year"],
        comparison["paper_indirect_share"],
        color=gray,
        linewidth=2.5,
        label="2025 paper (digitized)",
    )
    axes[1].plot(
        comparison["year"],
        comparison["indirect_share_proxy"],
        color=orange,
        linewidth=2.2,
        label="Paper-scope proxy (old-kit exclusions)",
    )
    axes[1].plot(
        comparison["year"],
        comparison["indirect_share_broad"],
        color=navy,
        linewidth=1.6,
        linestyle="--",
        label="Broad balance-sheet denominator",
    )
    axes[1].set_title("Share behind the veil")
    axes[1].set_ylabel("Fraction of household financial assets")

    for axis in axes:
        axis.set_xlabel("Year")
        axis.grid(axis="y", alpha=0.22)
        axis.spines[["top", "right"]].set_visible(False)
        axis.tick_params(colors=navy)
        axis.title.set_color(navy)
    handles, labels = [], []
    for axis in axes:
        new_handles, new_labels = axis.get_legend_handles_labels()
        for handle, label in zip(new_handles, new_labels, strict=True):
            if label not in labels:
                handles.append(handle)
                labels.append(label)
    figure.legend(
        handles,
        labels,
        loc="lower center",
        ncol=2,
        frameon=False,
        fontsize=9,
    )
    figure.suptitle(
        "Figure 1: authors-data level match, denominator remains version-specific",
        color=navy,
        fontsize=13,
        fontweight="bold",
    )
    figure.tight_layout(rect=(0, 0.15, 1, 0.94))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(figure)


def write_macros(comparison: pd.DataFrame, output_path: Path) -> None:
    """Write generated values used by the report and Beamer deck."""

    start = comparison.iloc[0]
    end = comparison.iloc[-1]
    level_mae = comparison["level_error"].abs().mean()
    share_proxy_mae = comparison["share_proxy_error"].abs().mean()
    share_broad_mae = comparison["share_broad_error"].abs().mean()
    level_corr = comparison[
        [
            "paper_indirect_assets_to_national_income",
            "indirect_assets_to_national_income",
        ]
    ].corr().iloc[0, 1]
    lines = [
        "% Generated by Code/scripts/build_figure1_authors_data.py. Do not edit.",
        f"\\newcommand{{\\AuthorFigureStartYear}}{{{int(start['year'])}}}",
        f"\\newcommand{{\\AuthorFigureEndYear}}{{{int(end['year'])}}}",
        f"\\newcommand{{\\AuthorFigureStartLevel}}{{{100 * start['indirect_assets_to_national_income']:.1f}\\%}}",
        f"\\newcommand{{\\PaperDigitizedStartLevel}}{{{100 * start['paper_indirect_assets_to_national_income']:.1f}\\%}}",
        f"\\newcommand{{\\AuthorFigureEndLevel}}{{{100 * end['indirect_assets_to_national_income']:.1f}\\%}}",
        f"\\newcommand{{\\PaperDigitizedEndLevel}}{{{100 * end['paper_indirect_assets_to_national_income']:.1f}\\%}}",
        f"\\newcommand{{\\AuthorFigureLevelMAE}}{{{100 * level_mae:.1f} pp}}",
        f"\\newcommand{{\\AuthorFigureLevelCorrelation}}{{{level_corr:.3f}}}",
        f"\\newcommand{{\\AuthorFigureShareProxyMAE}}{{{100 * share_proxy_mae:.1f} pp}}",
        f"\\newcommand{{\\AuthorFigureShareBroadMAE}}{{{100 * share_broad_mae:.1f} pp}}",
        "",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """Run the complete authors-data Figure 1 build."""

    balance_sheet = load_author_balance_sheet(
        AUTHOR_DATA / "fof" / "LQpanel_2019Q1.dta"
    )
    allocations = load_author_allocations(
        AUTHOR_DATA / "finalfiles" / "Yunveilhhd.dta"
    )
    crsp_equity = aggregate_crsp_financial_equity(
        AUTHOR_DATA / "crsp" / "msf.dta"
    )
    national_income = load_author_national_income(
        AUTHOR_DATA / "finalfiles" / "YinequalityNIPAanalysis.dta"
    )
    authors = construct_authors_figure1(
        balance_sheet, allocations, crsp_equity, national_income
    )

    with tempfile.TemporaryDirectory(prefix="mss-figure1-") as directory:
        paper_image = extract_paper_figure(PAPER_PDF, Path(directory))
        paper = digitize_paper_figure(paper_image)
    comparison = build_comparison(authors, paper)

    AUTHORS_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    authors.to_csv(AUTHORS_OUTPUT, index=False)
    paper.to_csv(PAPER_OUTPUT, index=False)
    comparison.to_csv(COMPARISON_OUTPUT, index=False)
    plot_comparison(comparison, FIGURE_OUTPUT)
    write_macros(comparison, MACRO_OUTPUT)

    print(f"Wrote {AUTHORS_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {PAPER_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {COMPARISON_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {FIGURE_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {MACRO_OUTPUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
