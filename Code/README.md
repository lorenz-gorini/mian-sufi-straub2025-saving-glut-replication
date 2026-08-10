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

Build the independent Figure 1 reconstruction from the pinned Federal Reserve
FWTW and BEA/FRED national-income inputs:

```bash
python Code/scripts/build_figure1.py
```

This writes the analysis-ready annual series to
`Data/processed/figure1_indirect_household_ownership.csv` and the generated
chart to `Results_Proposal/figures/figure1_indirect_household_ownership.png`.
The result uses year-end balance sheets for 1963--2019. It is an independent
reconstruction using the June 2026 FWTW vintage, not an exact output from the
authors' unavailable 2025 code.

Build the authors-data Figure 1 reconstruction from the authors' February 2021
data snapshot:

```bash
python Code/scripts/build_figure1_authors_data.py
```

This reads selected Q4 Financial Accounts columns from
`LQpanel_2019Q1.dta`, the authors' prepared financial-bond allocations from
`Yunveilhhd.dta`, their supplied CRSP monthly file for the listed-financial-
equity extension, and their national-income series. It explicitly combines
nine household-intermediary claim groups and writes compact annual component,
digitized-benchmark, and comparison CSVs under `Data/processed/`, plus the
comparison chart under `Results_Proposal/figures/`. The common-input sample is
1963--2016 because the authors' national-income analysis file ends in 2016.

The 2025 paper has 23 intermediary sectors and 34 instruments. The old kit
does not include those completed bilateral matrices, so the level comparison
is a close old-vintage authors-data reconstruction while the share denominator remains an
explicit proxy. See `docs/data/figure1-data.md` for the exact component and
denominator contracts.

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
