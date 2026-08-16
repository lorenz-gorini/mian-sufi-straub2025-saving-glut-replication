# Rich Saving Glut Replication

This workspace is for an independent, selective replication of the main results
in Mian, Straub, and Sufi's saving-glut project. The objective is not to rerun
every file in the authors' package. It is to understand the measurement,
accounting, and empirical steps well enough to reproduce a small set of central
results with transparent, documented code.

## Start here

1. Read [`AGENTS.md`](AGENTS.md) for the research objective, source hierarchy,
   project structure, and working rules.
2. Read [`docs/project/progress.md`](docs/project/progress.md) before starting
   substantial work. It is the only authoritative task dashboard.
3. Read the task record linked by the dashboard when a task spans multiple
   sessions or contains methodological decisions.
4. Read the compact
   [`author-kit quickstart`](docs/reference/author-kit-quickstart.md) before
   using the authors' package; consult the detailed
   [`author-kit map`](docs/reference/author-kit-map.md) only when a result needs
   a deeper code or data trace.

## Reproduce Figures 1, 5, 6, and 8

Run every command in this section from the project root unless it explicitly
changes directory. The detailed pipeline descriptions and output inventories
are in [`Code/README.md`](Code/README.md); this section is the shortest complete
route from restored inputs to the headline figures.

### 1. Create the Python environment

The implementation requires Python 3.13 or later. The following portable setup
creates an isolated environment from the dependencies declared in
`pyproject.toml`:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --editable ".[test]"
```

Development was validated with the `general` conda environment recorded in
`Code/README.md`, but that machine-specific environment name is not required.
The builds use NumPy, pandas, and Matplotlib. Poppler's `pdfimages` command is
also required because the paper curves are extracted and digitized only as
external comparison benchmarks. Digitized paper values never enter a
reconstructed series. A TeX distribution with `latexmk` is required only to
rebuild the final PDF.

### 2. Restore the non-Git inputs

The Git repository alone is not sufficient to rerun the empirical builds. Put
the following immutable inputs at their documented project-relative paths:

- the February 2021 author package under `MSS2021Febreplicationkit/`;
- the July 2025 paper at `MSS_SGR_July242025.pdf`;
- the pinned Federal Reserve FWTW file under `Data/raw/fwtw/`, using the URL
  and SHA-256 checksum in [`Data/raw/README.md`](Data/raw/README.md).

The small pinned national-income CSV is already tracked under
`Data/raw/national_income/`; its source and checksum are recorded in the same
raw-data README.

Figure 1 also uses preserved copies of two supplied final files as validation
and denominator inputs. On a fresh checkout, create that small project-owned
boundary from the downloaded package:

```bash
mkdir -p Data/processed/finalfiles
cp MSS2021Febreplicationkit/data/finalfiles/Yunveilhhd.dta \
  Data/processed/finalfiles/
cp MSS2021Febreplicationkit/data/finalfiles/YinequalityNIPAanalysis.dta \
  Data/processed/finalfiles/
```

Do not run the authors' master Stata script in place: it writes with `replace`.
The Python pipelines below read the restored author files but write only under
project-owned `Data/`, `Results_Proposal/`, `Presentation/`, and report
folders.

### 3. Run the figure builds

#### Figure 1: indirect household ownership

The headline build is the old-input reconstruction of the July 2025
definition:

```bash
python Code/scripts/build_figure1_authors_data.py
```

Headline output:
`Results_Proposal/figures/figure1_authors_data_comparison.png`.
The separate newer-public-data robustness result is produced by:

```bash
python Code/scripts/build_figure1.py
```

These two builds answer different questions and must not be merged or
silently relabelled. See [`docs/data/figure1-data.md`](docs/data/figure1-data.md).

#### Figure 5: saving by wealth group

```bash
python Code/scripts/build_figure5_authors_data.py
```

Headline output:
`Results_Proposal/figures/figure5_authors_data_comparison.png`.
The build reconstructs active saving from balance sheets and valuation changes,
closes aggregate saving to NIPA, takes trailing ten-year means, and subtracts
the 1982 level. See [`docs/data/figure5-data.md`](docs/data/figure5-data.md).

#### Figure 6: saving rates across the wealth distribution

The first command is a one-time preprocessing step over the supplied 16 GB raw
DINA file. It reads in bounded chunks and writes a much smaller validated share
table. If `Data/interim/figure6_percentile_shares.csv` already exists from the
same input vintage, only the second command is needed.

```bash
python Code/scripts/build_figure6_percentile_shares.py
python Code/scripts/build_figure6_authors_data.py
```

Headline output:
`Results_Proposal/figures/figure6_authors_data_comparison.png`.
The same build also produces the wealth-level diagnostic, digitization audit,
five-year evolution paths, and heatmap used in the referee report. See
[`docs/data/figure6-data.md`](docs/data/figure6-data.md).

#### Figure 8: net household debt by wealth group

Figure 8 deliberately keeps three routes separate. Run them in this order,
then build the common comparison:

```bash
python Code/scripts/build_figure8_authors_data.py
python Code/scripts/build_figure8_2021_direct.py
python Code/scripts/build_figure8_public_fwtw.py
python Code/scripts/build_figure8_method_comparison.py
```

Headline output: `Results_Proposal/figures/figure8_method_comparison.png`.
The first route is the 2021-kit seven-round lineage benchmark, the second is
the primary same-vintage direct-cell/full-Leontief reconstruction, and the
third is a mixed-vintage public-FWTW robustness exercise. None is an exact
reproduction of the unavailable July 2025 34-instrument-by-27-sector matrix.
See [`docs/data/figure8-2021-direct-data.md`](docs/data/figure8-2021-direct-data.md)
and [`docs/data/figure8-public-fwtw-data.md`](docs/data/figure8-public-fwtw-data.md).

### 4. Validate and rebuild the written submission

Run the full test suite after rebuilding the figures:

```bash
python -m pytest -q
```

To regenerate the report-facing values and the combined submission from the
verified empirical outputs:

```bash
python Code/scripts/build_replication_summary_assets.py
python Code/scripts/build_debt_composition_extension.py
python Code/scripts/build_extension_proposal_assets.py
cd Submission_Report
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -jobname=submission_report main.tex
```

The final artifact is `Submission_Report/submission_report.pdf`. Return to the
project root before running further project-relative commands.

## Current state

The project has been initialized, the authors' package has been mapped, and the
Leontief unveiling operator has been implemented and tested. Figure 1 now has
a selective authors-data reconstruction plus a separate newer-public-data
robustness result; see `docs/project/progress.md` for the precise evidence
boundary. The authoritative target
paper is the 66-page July 25, 2025 draft
`MSS_SGR_July242025.pdf`. The paper states that it is a
heavily revised version of the earlier draft titled *The Saving Glut of the Rich
and the Rise in Household Debt*. `MSS2021Febreplicationkit/` corresponds to that
earlier version, so it is a valuable but non-identical implementation reference.
Figure numbers, dates, methodology, and results must be crosswalked rather than
assumed to match.

The compact replication submission artifacts are now available as the editable
17-slide `Presentation/5_replication_submission/presentation.pptx` and the
seven-page `Submission_Report/submission_report.pdf`, which combines the
referee report, compact replication summary, and extension proposal. The
longer `Report/report.tex` remains the detailed technical companion.

`NotebookLM-Present-Unveiling_the_Rich_Saving_Glut.pdf` is a
15-page, image-only NotebookLM synthesis of the newer paper. Use it for
orientation only.

The approved core replication scope is Figures 1, 5, and 8. Figure 6 was added
as a verified diagnostic for the referee report, while Figure 9 remains a
time-permitting extension. The project is explicitly learning-first: equations,
economic intuition, units, sign conventions, assumptions, and data lineage must
be explained in markdown and summarized in a consistent visual presentation as
the code is developed.

## Main folders

| Path | Purpose |
| --- | --- |
| `MSS_SGR_July242025.pdf` | Authoritative July 25, 2025 target paper. |
| `MSS2021Febreplicationkit/` | Authors' code, data, and outputs. Treat as read-only reference material. |
| `Code/` | This project's independent implementation, tests, and exploratory notebooks. |
| `Data/` | This project's data artifacts. See `docs/data/data-guide.md` before adding files. |
| `Results_Proposal/` | Candidate and selected replication targets, acceptance criteria, and result-level notes. |
| `Presentation/` | A concise, reproducible progress presentation for discussion and feedback. |
| `Report/` | The living LaTeX course report; include only documented and verified methods or results. |
| `Referee_Report/` | Editable referee-report source, reproducible build scripts, and local submission files. |
| `Submission_Report/` | Final combined LaTeX entry point and written-submission artifact. |
| `docs/` | Canonical project, data, and reference documentation. |

## Repository boundary

Git tracks the project's documentation, code, tests, editable report and
presentation sources, and compact submission PDFs. It deliberately does not
redistribute the authors' 45 GB replication package, external paper PDFs,
large downloadable raw data, copied or generated datasets, caches, or
temporary render output. These local inputs retain the paths used throughout
the documentation:

- place the February 2021 author package at `MSS2021Febreplicationkit/`;
- place the authoritative target paper at `MSS_SGR_July242025.pdf`; and
- obtain the pinned public inputs described, with checksums, in
  [`Data/raw/README.md`](Data/raw/README.md).

This boundary keeps the Git history reviewable without weakening provenance:
source versions, retrieval dates, checksums, producing scripts, and generated
output paths remain documented in the tracked files.
