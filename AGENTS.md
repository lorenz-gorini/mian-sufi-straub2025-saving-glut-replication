# AGENTS.md

High-level orientation for humans and AI agents working in this repository.
This is the canonical agent brief. Keep task status in
[`docs/project/progress.md`](docs/project/progress.md), detailed multi-session
decisions in `docs/project/tasks/`, and per-module behavior in code docstrings.
Do not duplicate those details here.

## 1. Research objective

Independently reproduce a deliberately small set of the major empirical results
from Mian, Straub, and Sufi's saving-glut project. The purpose is methodological
understanding, not mechanical execution of the full authors' package.

The replication should make the following chain explicit:

1. which economic claim and paper exhibit are being replicated;
2. which raw or prepared sources identify the required objects;
3. how the data are cleaned, transformed, and merged;
4. how saving, valuation changes, wealth groups, and final asset holdings are
   measured;
5. which computation or model generates the exhibit; and
6. how closely the independent result matches the authors' result.

The project is a course replication, not a new research paper. Produce readable
code, data documentation, reproducible figures and tables, and a compact
presentation. Do not create paper-style prose unless explicitly requested.

### Learning-first collaboration

This is an instructive exercise. The user wants to understand the economics,
measurement, and methodology rather than receive a finished black-box
replication. A technically correct result is not sufficient if the reasoning is
opaque.

For every substantive step, agents must:

1. state the economic question and why the step is needed;
2. introduce the relevant equation before or alongside its implementation;
3. define every symbol, unit, sign convention, normalization, and maintained
   assumption;
4. connect each data transformation to the economic object it measures;
5. use a small balance-sheet, matrix, or numerical example when it materially
   improves intuition;
6. explain the identifying/accounting invariant and how the code verifies it;
7. implement the step in readable, reviewable increments; and
8. record the durable explanation in markdown and summarize it visually in the
   presentation.

Do not hide core logic behind premature abstraction. Once a step is understood
and verified, refactor repeated logic into a well-named function with an
explicit contract. When code names differ from paper notation, maintain a clear
mapping rather than switching terminology silently.

## 2. Source hierarchy and version relationship

Use sources in this order:

1. **Target article:** `MSS_SGR_July242025.pdf`, a 66-page draft dated July 25,
   2025, is authoritative for claims, definitions, sample periods, equations,
   and exhibit numbers. A parsed Markdown copy is already available at
   `/Users/lorenzogorini/Library/CloudStorage/OneDrive-UniversitàCommercialeLuigiBocconi/PhD/research-wiki/papers/inequality/mian-2025-saving-glut-rich/full.md`.
   Use that file first for text search, quotation lookup, and section reading;
   do not parse the PDF again merely because a user asks to read the paper.
   Return to the PDF only when pagination, equations, figures, footnotes, or
   visual layout must be checked against the authoritative artifact.
2. **Authors' February 2021 replication package:** authoritative only for what
   the supplied older code and data actually do. The 2025 paper explicitly
   describes itself as a heavily revised version of the earlier draft titled
   *The Saving Glut of the Rich and the Rise in Household Debt*, which is the
   version named in the kit. Start with
   `MSS2021Febreplicationkit/readme.pdf`,
   `MSS2021Febreplicationkit/mss_savingglut_master.do`, and
   `MSS2021Febreplicationkit/code/mss_analysis.do`.
3. **Attached synthesis:** `Unveiling_the_Rich_Saving_Glut.pdf` is useful for
   orientation only. It is a 15-page, image-only NotebookLM synthesis of the
   2025 paper. Do not cite the synthesis as the paper.
4. **This project's documentation and code:** authoritative for our choices,
   implementation, and current status.

The target paper uses data through 2019 and a matrix/Leontief-style unveiling
framework, while the older kit generally ends in 2016 and implements an earlier
round-by-round unveiling procedure. If the paper and code differ, document the
discrepancy and build an explicit crosswalk. Never assign an older exhibit to a
2025 exhibit based on a similar caption alone, and never infer an undocumented
definition from a variable name.

## 3. What "independent replication" means here

Work in three explicit layers:

1. **Benchmark:** reproduce an exhibit from the authors' supplied final files.
   This verifies that the exhibit definition and plotting/statistical logic
   have been understood.
2. **Reconstruction:** rebuild the necessary analysis dataset from the earliest
   feasible supplied inputs, documenting transformations and merge contracts.
3. **Independent result:** produce the selected figure or table from our code
   and compare it with the benchmark using declared tolerances.

Do not present layer 1 as an independent replication. For a selected result,
state clearly how far upstream the reconstruction goes and why. Some state-level
inputs are unavailable publicly; the package read-me says that precomputed
state-level files are supplied for this reason.

`MSS2021Febreplicationkit/` is read-only reference material. Do not edit its
code, data, final files, or outputs, and do not run its master script in place:
the Stata code uses `replace` extensively. If an original-code benchmark is
needed, use an isolated copy and record the exact Stata version and packages.

## 4. Project map

```text
.
├── AGENTS.md                         # canonical agent brief
├── README.md                         # human entry point
├── MSS_SGR_July242025.pdf            # authoritative target paper
├── Unveiling_the_Rich_Saving_Glut.pdf
├── MSS2021Febreplicationkit/         # read-only authors' materials
├── Code/                             # our implementation
├── Data/                             # our raw/interim/processed artifacts
├── Results_Proposal/
│   └── major_results.md              # candidate and chosen exhibits
├── Presentation/
│   └── README.md                     # progress-deck conventions
└── docs/
    ├── README.md                     # documentation index
    ├── data/data-guide.md            # data zones and documentation contract
    ├── project/progress.md           # sole task dashboard
    ├── project/tasks/                # result-selection and presentation records
    └── reference/author-kit-map.md   # map of authors' code and outputs
```

Create subfolders under `Code/` and `Data/` only when the first real artifact
needs them. Avoid empty architecture and one-file catch-all modules.

## 5. Required workflow

Before substantial work:

1. read `docs/project/progress.md`;
2. identify the owning task and read its task record, if present;
3. inspect the relevant paper passage and authors' code;
4. state the input, output, unit of observation, keys, and expected invariant;
5. update the dashboard and task record with material progress in the same
   change.

For each selected result, maintain a reproducibility record containing:

- paper claim and exhibit identifier;
- paper version and page;
- authors' output file and analysis-code lines;
- required source and intermediate datasets;
- sample restrictions, units, transformations, and weighting;
- benchmark values or digitized series;
- independent output path;
- comparison metric, tolerance, result, and remaining discrepancy.

Never mark a task complete without checking its definition of done and linking
the evidence.

## 6. Data and schema rules

Read [`docs/data/data-guide.md`](docs/data/data-guide.md) before touching data.

- Treat authors' raw and final data as immutable.
- Write our artifacts only under `Data/`, `Results_Proposal/`,
  `Presentation/`, or another project-owned output path.
- Preserve provenance. A processed dataset must identify its inputs and the
  script/configuration that created it.
- Document every analysis dataset's unit of observation, primary key, time
  coverage, column meanings, dtypes, units, missingness, and source.
- Specify merge cardinality before merging and assert it in code. Report
  matched, left-only, and right-only counts when economically relevant.
- Validate required columns, keys, types, ranges, and configuration once at the
  boundary. Downstream code should trust the validated representation.
- Raise a clear error on structural inconsistency. Do not continue with missing
  required columns, duplicate primary keys, impossible periods, or ambiguous
  units.
- Distinguish zeros from missing values and stocks from flows. State whether
  monetary variables are nominal, real, levels, shares of national income, or
  changes relative to a base period.

## 7. Code standards

The primary implementation language is Python unless the task explicitly
requires a Stata benchmark.

Repository Markdown is previewed with VS Code's built-in KaTeX renderer. Use
`$...$` for inline math and `$$...$$` on separate lines for display math; do
not use `\(...\)` or `\[...\]` as math delimiters because VS Code does not
document them as supported delimiters. Escape literal currency signs as `\$`.

- Use readable, Pythonic, non-redundant code with PEP 8 naming.
- Prefer `pathlib.Path`, explicit configuration, type hints, and small
  single-purpose functions.
- Public functions/classes and nontrivial private helpers need NumPy-style
  docstrings. Document DataFrame contracts, units, side effects, randomness,
  and raised exceptions.
- Separate reusable transformations from entry-point scripts. Notebooks are for
  exploration and must not become hidden pipeline dependencies.
- Use deterministic seeds for randomized work.
- Do not hardcode this machine's absolute project path in code. Resolve paths
  from a project root or explicit configuration.
- Add tests for nontrivial transformations, accounting identities, merge
  contracts, and period/group construction.
- Prefer exact failures over defensive fallback chains. Do not check the same
  invariant repeatedly at multiple layers.

When a Python environment is selected, record it in `Code/README.md` and use
that interpreter consistently for Python, package installation, and tests. Do
not assume the environment used by another project.

## 8. Results and presentation

Results are markdown-first during exploration. Record interpretations and open
questions in `Results_Proposal/` or the relevant task record. Numerical values
must remain generated by code; do not hand-edit result tables.

Export figures and tables to stable, descriptive paths and record the producing
script. The presentation is a compact visual teaching companion and progress
deck, not a second source of truth. Follow
[`Presentation/README.md`](Presentation/README.md):

- 16:9, minimal academic style;
- one claim or methodological idea per slide;
- relevant equations with all notation, units, and sign conventions defined;
- intuitive diagrams or small worked examples for difficult constructions;
- generated figures/tables rather than copied values;
- brief source and sample notes on every empirical slide;
- appendix slides for diagnostics and robustness;
- explicit labels for benchmark, reconstructed, and independently replicated
  outputs.

## 9. Current direction

The replication scope approved by the user is:

1. **Figure 1 - core:** learn and reproduce the financial-network unveiling
   methodology and the rise in indirect household ownership;
2. **Figure 5 - core:** learn and reproduce the measurement of the saving glut
   of the top 1 percent;
3. **Figure 8 - core:** learn and reproduce net household debt across the wealth
   distribution; and
4. **Figure 9 - time-permitting extension:** convert the Figure 8 debt stocks
   into financing flows.

T-001 remains active only to complete the old/new code and data lineage for
these exhibits. Do not broaden the empirical scope before the three core
figures are understood, documented, implemented, and verified.

See [`Results_Proposal/major_results.md`](Results_Proposal/major_results.md) and
[`docs/project/tasks/result-selection.md`](docs/project/tasks/result-selection.md).
The pedagogical presentation contract is in
[`docs/project/tasks/pedagogical-presentation.md`](docs/project/tasks/pedagogical-presentation.md).
