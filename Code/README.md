# Code

This folder will contain the independent implementation. Do not copy the
authors' Stata scripts here and translate them line by line. First specify the
economic object, data contract, and accounting identity; then implement the
minimum reusable transformation needed by the selected results.

The intended structure should emerge with the work:

- reusable package modules for data loading, transformations, measures,
  estimation, and plotting;
- thin entry-point scripts for reproducible stages;
- `tests/` for merge contracts, accounting identities, period/group
  construction, and nontrivial transformations;
- `notebooks/` only for disposable exploration.

When Python implementation begins, document the chosen interpreter/environment,
installation command, test command, and pipeline entry points here. Follow the
code and failure rules in [`../AGENTS.md`](../AGENTS.md).

## Current environment

- Interpreter: `/Users/lorenzogorini/anaconda3/envs/general/bin/python`
- Python: 3.13.2
- Core dependencies used so far: NumPy 2.1.3, pandas 2.2.3,
  Matplotlib 3.10.3, and pytest 8.4.2
- System dependency: Poppler's `pdfimages`, used only to regenerate the
  digitized paper-figure benchmark series
- Local distribution: `mss-saving-glut-replication`, installed in editable mode

Install the project once from the project root after activating the recorded
environment:

```bash
conda activate general
python -m pip install --editable ".[test]"
```

This is a standard editable package installation: `pyproject.toml` declares
the package and its dependencies, while Python imports the live source under
`Code/unveiling/`. Code changes therefore take effect without reinstalling.
The distribution name is `mss-saving-glut-replication`; its Python import name
is `unveiling`.

Run the tests from the project root:

```bash
python -m pytest -q
```

## Stata benchmark-figure formatting

`stata/format_2021_benchmark_figures.do` creates presentation-specific versions
of the authors' February 2021 Figures 7 and 9 without editing the authors'
package or overwriting its outputs. It reads the regenerated
`YinequalityFAanalysis.dta` and writes PDF, EPS, and rendered PNG assets under
`Presentation/1_replication_package_validation/assets/`.

The plotted variables and transformations match the authors' figure blocks.
Only legend placement, graph dimensions, label sizing, and background are
changed so the plotting area remains wide enough for a fair side-by-side
comparison with the 2025 paper. The script validates the year key, required
variables, 1982 base observations, and nonempty plotted samples before export.

Run the small worked example:

```bash
python Code/examples/leontief_unveiling.py
```

The example prints the complete direct matrix, its $B$ and $Q$ blocks, the
unveiled matrix, the two household fixed-point equations, and the first six
bank-to-household path contributions. This is the numerical source for the
exact network shown in the presentation and report.

Regenerate the presentation's numerical example values:

```bash
python Code/scripts/build_unveiling_teaching_assets.py
```

## Figure 1 pipelines: keep these separate

The two Figure 1 builds estimate the same economic object but answer different
empirical questions. They share no input files and write no common output.

| Role | Primary authors-kit reconstruction | Secondary public-data robustness |
| --- | --- | --- |
| Question | How closely can the July 2025 Figure 1 definition be reconstructed from the authors' supplied older inputs? | Does the same aggregate pattern remain visible in a later, easily obtainable public vintage? |
| Entry point | `Code/scripts/build_figure1_authors_data.py` | `Code/scripts/build_figure1.py` |
| Reusable module | `Code/unveiling/figure1_authors.py` | `Code/unveiling/figure1.py` |
| Inputs | February 2021 kit Q4 panel and CRSP; preserved final files only under the documented validation/denominator boundary | Pinned June 2026 Federal Reserve FWTW CSV and BEA/FRED national income |
| Sample | 1963--2016 | 1963--2019 |
| Processed result | `Data/processed/figure1_authors_data.csv` plus comparison and bond-validation files | `Data/processed/figure1_indirect_household_ownership.csv` |
| Figure | `Results_Proposal/figures/figure1_authors_data_reconstruction.png` (standalone) and `figure1_authors_data_comparison.png` (benchmark comparison) | `Results_Proposal/figures/figure1_indirect_household_ownership.png` |
| Correct label | Primary old-input reconstruction of the 2025 definition | Secondary newer-public-data robustness exercise |

Do not merge the annual series or substitute one pipeline's inputs into the
other. Compare their generated outputs only after preserving their vintage,
sector, denominator, and equity-extension labels.

Build the secondary newer-public-data robustness result from the pinned
Federal Reserve FWTW and BEA/FRED national-income inputs:

```bash
python Code/scripts/build_figure1.py
```

This writes the analysis-ready annual series to
`Data/processed/figure1_indirect_household_ownership.csv` and the generated
chart to `Results_Proposal/figures/figure1_indirect_household_ownership.png`.
The result uses year-end balance sheets for 1963--2019. It is an independent
robustness reconstruction using the June 2026 FWTW vintage, not an exact output
from the authors' unavailable 2025 code and not a replacement for the
authors-kit build below.

Build the primary Figure 1 reconstruction from the authors' February 2021 data
snapshot:

```bash
python Code/scripts/build_figure1_authors_data.py
```

This reads selected Q4 Financial Accounts columns from
`LQpanel_2019Q1.dta` and reimplements in Python the authors' proportional
missing-cell allocations for four financial-intermediary bond categories. It
also rebuilds the household equity share from that panel and combines it with
the supplied raw CRSP monthly file. The preserved `Data/processed/finalfiles/`
copy of `Yunveilhhd.dta` is used only to validate those reconstructed cells and
to supply three nonfinancial exclusions for an explicitly approximate share
denominator; its old unveiling output never enters the Figure 1 numerator.
`YinequalityNIPAanalysis.dta` supplies national income. The script writes the
annual components, bond-cell validation, digitized benchmark, and aligned
comparison under `Data/processed/`, plus the chart under
`Results_Proposal/figures/`. The common-input sample is 1963--2016 because the
authors' national-income analysis file ends in 2016.

The 2025 paper has 23 intermediary sectors and 34 instruments. The old kit
does not include those completed bilateral matrices, so the level comparison
is a close old-vintage authors-data reconstruction while the share denominator
remains an explicit proxy. See `docs/data/figure1-data.md` and
`docs/project/tasks/figure1-replication.md` for the exact component,
validation, and denominator contracts.

## Figures 5 and 8 from authors-kit inputs

Build the July 2025 Figure 5 saving procedure on the February 2021 inputs:

```bash
python Code/scripts/build_figure5_authors_data.py
```

This starts upstream of the final saving series. It allocates 29 aggregate
balance-sheet categories using the supplied fine DINA shares, applies housing
and debt valuation factors, solves the residual equity return that closes to
NIPA personal plus business saving, and then applies the paper's trailing
ten-year mean and 1982 normalization. The annual sample is 1963--2016 and the
display sample is 1972--2016. See `docs/data/figure5-data.md`.

Build the best-feasible Figure 8 debt proxy:

```bash
python Code/scripts/build_figure8_authors_data.py
```

This aggregates the package's fine-cohort household-debt assets after the old
seven-round unveiling, subtracts positive debt liabilities, divides by
national income, and subtracts the 1982 level. It is intentionally named and
labelled a proxy because the package lacks the completed annual matrices
required to rerun the revised 2025 augmented Leontief solve. See
`docs/data/figure8-data.md`.

Both scripts digitize their 2025 paper figures only to create external
comparison series. Digitized values never enter the empirical calculations.
The complete test suite covers wealth-group partitions, NIPA closure, moving
window/base-year construction, debt signs, and fine-to-coarse aggregation.

## Leontief unveiling

`unveiling.DirectOwnershipNetwork` is the minimal implementation of Sections
2.1--2.2 of the 2025 paper. It preserves the paper's issuer-row,
holder-column orientation and implements:

- Equation (4): construct the direct ownership matrix from completed
  instrument-level dollar holdings;
- Equation (1): unveil arbitrarily long intermediary chains;
- Equation (2): recover sector net worth from liabilities and direct holdings;
- Equation (3): allocate primary assets to ultimate owners.

The durable economic explanation, array contracts, maintained assumptions, and
comparison with the authors' February 2021 Stata procedure are in
[`../docs/methods/leontief-unveiling.md`](../docs/methods/leontief-unveiling.md).
